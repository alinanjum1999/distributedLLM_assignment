import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login

def authenticate_huggingface():
    hf_api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    print (hf_api_token)
    if not hf_api_token:
        raise ValueError("Hugging Face API token is not set. Please set the HUGGINGFACE_API_TOKEN environment variable.")
    
    login(token=hf_api_token, add_to_git_credential=False)
    print("Authenticated with Hugging Face")

def preload_and_save_model(model_name, save_dir):
    if model_name == "llama2":
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
        model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    elif model_name == "mistral":
        tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
        model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
    else:
        raise ValueError(f"Unsupported model: {model_name}")

    # Save the model and tokenizer locally
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    print(f"Model {model_name} saved to {save_dir}")

def main():
    authenticate_huggingface()

    # Preload Llama2 model
    llama2_dir = "./preloaded_models/llama2"
    preload_and_save_model("llama2", llama2_dir)

    # Preload Mistral model
    mistral_dir = "./preloaded_models/mistral"
    preload_and_save_model("mistral", mistral_dir)

if __name__ == "__main__":
    main()
