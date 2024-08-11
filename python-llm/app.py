from flask import Flask, request, jsonify
from model_utils import load_model, generate_response

app = Flask(__name__)

# Initialize the conversation storage
conversations = {}

@app.route('/select-model', methods=['POST'])
def select_model():
    """Endpoint to select the model (Llama2 or Mistral)."""
    data = request.json
    model_name = data.get('model')
    
    try:
        model = load_model(model_name)
        conversation_id = str(len(conversations) + 1)
        conversations[conversation_id] = {
            'model_name': model_name,
            'model': model,
            'history': []
        }
        return jsonify({"conversation_id": conversation_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/query', methods=['POST'])
def query():
    """Endpoint to send a query to the selected model."""
    data = request.json
    conversation_id = data['conversation_id']
    query_text = data['query']

    if conversation_id not in conversations:
        return jsonify({"error": "Invalid conversation ID"}), 400

    model = conversations[conversation_id]['model']
    try:
        response = generate_response(model, query_text)
        # Store in history
        conversations[conversation_id]['history'].append({"query": query_text, "response": response})

        return jsonify({"response": response, "conversation_id": conversation_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
