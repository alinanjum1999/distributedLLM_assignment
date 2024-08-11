import os
from transformers import AutoModelForCausalLM, AutoTokenizer



def load_model(model_name):
    """Load the specified model from Hugging Face."""
    hf_api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    
    try:
        if model_name == "llama2":
            model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-chat-hf', use_auth_token=hf_api_token)
        elif model_name == "mistral":
            model = AutoModelForCausalLM.from_pretrained('mistralai/Mistral-7B-v0.1', use_auth_token=hf_api_token)
        else:
            # Load a default model (e.g., gpt2) for testing purposes
            model = AutoModelForCausalLM.from_pretrained('gpt2', use_auth_token=hf_api_token)
        return model
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        raise

def generate_response(model, query):
    """Generate a response from the model based on the input query."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model.config.name_or_path, use_auth_token=os.getenv('HUGGINGFACE_API_TOKEN'))
        inputs = tokenizer(query, return_tensors="pt")
        outputs = model.generate(**inputs)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        raise
