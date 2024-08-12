import os
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_saved_model(model_name, model_dir):
    """Load the model and tokenizer from the saved directory."""
    try:
        model_path = os.path.join(model_dir, model_name)
        model = AutoModelForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        return model, tokenizer
    except Exception as e:
        print(f"Error loading model '{model_name}' from '{model_dir}': {e}")
        raise

def generate_response(model, tokenizer, query):
    """Generate a response from the model based on the input query."""
    try:
        inputs = tokenizer(query, return_tensors="pt")
        outputs = model.generate(**inputs)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        raise
