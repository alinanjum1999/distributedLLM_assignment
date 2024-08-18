import panel as pn
from ctransformers import AutoModelForCausalLM
import sqlite3
import os
import uuid
import asyncio

pn.extension()

# Define model arguments for Llama2 and Mistral
MODEL_ARGUMENTS = {
    "llama": {
        "args": ["TheBloke/Llama-2-7b-Chat-GGUF"],
        "kwargs": {"model_file": "llama-2-7b-chat.Q5_K_M.gguf"},
    },
    "mistral": {
        "args": ["TheBloke/Mistral-7B-Instruct-v0.1-GGUF"],
        "kwargs": {"model_file": "mistral-7b-instruct-v0.1.Q4_K_M.gguf"},
    },
}

# Create a model selection dropdown
model_selector = pn.widgets.Select(name="Select Model", options=["Llama2", "Mistral"])

# Define the maximum context length
MAX_CONTEXT_LENGTH = 512

# Initialize database connection
conn, cursor = None, None
current_db_file = None

# Directory to store conversation databases
CONVERSATION_DIR = "conversations"
if not os.path.exists(CONVERSATION_DIR):
    os.makedirs(CONVERSATION_DIR)

# Initialize the stop_event for managing the stopping of response generation
stop_event = asyncio.Event()  # This ensures that stop_event is defined and can be accessed globally

# Function to connect to the user's database
def connect_to_user_db(user_name):
    global conn, cursor, current_db_file
    db_file = os.path.join(CONVERSATION_DIR, f'{user_name}_chatbot.db')
    if current_db_file != db_file:
        if conn:
            conn.close()
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        current_db_file = db_file
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                user_name TEXT,
                model_name TEXT,
                user_message TEXT,
                model_response TEXT
            )
        ''')
        conn.commit()

# Function to save conversation history
def save_conversation(conversation_id, user_name, model_name, user_message, model_response):
    cursor.execute('''
        INSERT INTO conversations (conversation_id, user_name, model_name, user_message, model_response)
        VALUES (?, ?, ?, ?, ?)
    ''', (conversation_id, user_name, model_name, user_message, model_response))
    conn.commit()

# Function to load conversations by user name
def load_conversations_by_user(user_name):
    cursor.execute('''
        SELECT conversation_id, user_message, model_response FROM conversations WHERE user_name=?
    ''', (user_name,))
    return cursor.fetchall()

# Function to apply sliding window truncation
def apply_sliding_window(full_context, max_context_length):
    tokens = full_context.split()
    if len(tokens) > max_context_length:
        return " ".join(tokens[-max_context_length:])
    return full_context

# Generate a unique conversation ID
conversation_id = str(uuid.uuid4())

# Create buttons and widgets
reset_button = pn.widgets.Button(name="Reset Conversation", button_type="warning")
stop_button = pn.widgets.Button(name="Stop Generating", button_type="danger")
user_name_input = pn.widgets.TextInput(name="Enter Your Name", placeholder="Type your name here...")
load_conversations_button = pn.widgets.Button(name="Load Conversations", button_type="primary")
input_box = pn.widgets.TextInput(name="Your Message")
output_area = pn.pane.Markdown("Chatbot responses will appear here.", height=300, width=500)

# Function to reset conversation history
def reset_conversation(event):
    global conversation_id
    conversation_id = str(uuid.uuid4())
    output_area.object = "Conversation history has been reset."

reset_button.on_click(reset_conversation)

# Function to stop response generation
def stop_generation(event):
    stop_event.set()  # This will stop the response generation when the button is clicked

stop_button.on_click(stop_generation)

# Function to load conversations
def load_conversations(event):
    user_name = user_name_input.value
    if not user_name:
        output_area.object = "Please enter your name to load conversations."
        return
    connect_to_user_db(user_name)
    conversations = load_conversations_by_user(user_name)
    if conversations:
        output_area.object = f"Loaded past conversations for {user_name}:"
        for conversation in conversations:
            user_message = conversation[1]
            model_response = conversation[2]
            output_area.object += f"\n\n**You**: {user_message}\n\n**Chatbot**: {model_response}"
    else:
        output_area.object = f"No past conversations found for {user_name}."

load_conversations_button.on_click(load_conversations)

# Function to handle sending a message
def send_message(event):
    global stop_event
    stop_event.clear()
    user_message = input_box.value
    user_name = user_name_input.value or "Anonymous"
    selected_model = "llama" if model_selector.value == "Llama2" else "mistral"

    if user_message:
        # Connect to the user's database
        connect_to_user_db(user_name)

        # Save the user input to the conversation history
        save_conversation(conversation_id, user_name, selected_model, user_message, "")

        # Load the full conversation history for context
        cursor.execute('''
            SELECT user_message, model_response FROM conversations WHERE conversation_id=?
        ''', (conversation_id,))
        history = cursor.fetchall()
        full_context = " ".join([f"User: {h[0]} Model: {h[1]}" for h in history])
        full_context = apply_sliding_window(full_context, MAX_CONTEXT_LENGTH)

        # Load the selected model if not already cached
        if selected_model not in pn.state.cache:
            try:
                pn.state.cache[selected_model] = AutoModelForCausalLM.from_pretrained(
                    *MODEL_ARGUMENTS[selected_model]["args"],
                    **MODEL_ARGUMENTS[selected_model]["kwargs"],
                    gpu_layers=1  # Use GPU if available
                )
            except (FileNotFoundError, OSError) as e:
                print(f"GPU-related error encountered: {e}. Falling back to CPU.")
                pn.state.cache[selected_model] = AutoModelForCausalLM.from_pretrained(
                    *MODEL_ARGUMENTS[selected_model]["args"],
                    **MODEL_ARGUMENTS[selected_model]["kwargs"],
                    gpu_layers=0  # Force CPU usage
                )

        # Generate the complete response at once
        response_chunks = pn.state.cache[selected_model](
            full_context,
            temperature=0.7,
            top_k=50,
            stream=True
        )
        full_response = ""
        for chunk in response_chunks:
            if stop_event.is_set():
                break
            full_response += chunk

        # Display the response
        output_area.object += f"\n\n**You**: {user_message}\n\n**Chatbot**: {full_response}"

        # Save the chatbot's response to the conversation history
        if not stop_event.is_set():
            save_conversation(conversation_id, user_name, selected_model, "", full_response)

submit_button = pn.widgets.Button(name="Send", button_type="primary")
submit_button.on_click(send_message)

# Layout the input, button, and output
layout = pn.Column(
    pn.pane.Markdown("# 🗨️ Distributedllm Chatbot"),
    pn.Row(user_name_input, model_selector, sizing_mode="stretch_width"),
    pn.Row(reset_button, stop_button, load_conversations_button, sizing_mode="stretch_width"),
    pn.layout.Divider(),
    output_area,
    pn.Row(input_box, submit_button),
    sizing_mode="stretch_width"
)

# Make the layout servable
layout.servable()
