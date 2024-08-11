import os
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer

def authenticate_huggingface():
    """Authenticate with Hugging Face using the API token."""
    hf_api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    
    if hf_api_token:
        login(token=hf_api_token)
    else:
        # If no token is provided, prompt the user to log in manually
        login()

def load_model(model_name):
    """Load the specified model from Hugging Face."""
    authenticate_huggingface()

    try:
        if model_name == "llama2":
            # Replace with the correct model identifier for Llama2
            model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-hf')
        elif model_name == "mistral":
            # Replace with the correct model identifier for Mistral
            model = AutoModelForCausalLM.from_pretrained('mistralai/Mistral-7B-v0.1')
        else:
            # Default model for testing
            model = AutoModelForCausalLM.from_pretrained('gpt2')
        return model
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        raise

def generate_response(model, query):
    """Generate a response from the model based on the input query."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model.config.name_or_path)
        inputs = tokenizer(query, return_tensors="pt")
        outputs = model.generate(**inputs)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        raise
