import os
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

# Directory where models are preloaded and saved
models_dir = "./preloaded_models"

# In-memory storage for loaded models and tokenizers
loaded_models = {}

def load_model_from_disk(model_name):
    """Load the model and tokenizer from the preloaded models directory."""
    model_path = os.path.join(models_dir, model_name)
    
    if model_name not in loaded_models:
        try:
            model = AutoModelForCausalLM.from_pretrained(model_path)
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            loaded_models[model_name] = (model, tokenizer)
            print(f"Model '{model_name}' loaded from disk.")
        except Exception as e:
            print(f"Error loading model '{model_name}' from '{model_path}': {e}")
            raise
    else:
        print(f"Model '{model_name}' already loaded in memory.")
    
    return loaded_models[model_name]

@app.route('/select-model', methods=['POST'])
def select_model():
    """Endpoint to select the model and initialize conversation context."""
    data = request.json
    model_name = data.get('model')

    try:
        model, tokenizer = load_model_from_disk(model_name)
        conversation_id = str(len(loaded_models) + 1)
        loaded_models[conversation_id] = {
            'model_name': model_name,
            'model': model,
            'tokenizer': tokenizer,
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

    if conversation_id not in loaded_models:
        return jsonify({"error": "Invalid conversation ID"}), 400

    model = loaded_models[conversation_id]['model']
    tokenizer = loaded_models[conversation_id]['tokenizer']
    try:
        inputs = tokenizer(query_text, return_tensors="pt")
        outputs = model.generate(**inputs)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Store in history
        loaded_models[conversation_id]['history'].append({"query": query_text, "response": response})

        return jsonify({"response": response, "conversation_id": conversation_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
