import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

def authenticate_huggingface():
    """Authenticate with Hugging Face using the API token."""
    hf_api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    
    if hf_api_token:
        login(token=hf_api_token)
    else:
        raise ValueError("Hugging Face API token is not set. Please set the HUGGINGFACE_API_TOKEN environment variable.")

def preload_and_save_model(model_name, save_dir):
    """Load the model from Hugging Face and save it to the specified directory."""
    try:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Save the model and tokenizer
        model.save_pretrained(save_dir)
        tokenizer.save_pretrained(save_dir)
        
        print(f"Model '{model_name}' saved successfully to '{save_dir}'.")
    except Exception as e:
        print(f"Error loading or saving model '{model_name}': {e}")
        raise

def main():
    # Example: Preload Llama2 and Mistral models
    models_to_load = {
        "llama2": "meta-llama/Llama-2-7b-hf",
        "mistral": "kittn/mistral-7B-v0.1-hf"
    }

    # Directory to save preloaded models
    models_dir = "./preloaded_models"
    
    # Ensure the directory exists
    os.makedirs(models_dir, exist_ok=True)

    authenticate_huggingface()

    # Preload and save each model
    for model_name, hf_model_name in models_to_load.items():
        save_dir = os.path.join(models_dir, model_name)
        preload_and_save_model(hf_model_name, save_dir)

if __name__ == "__main__":
    main()
