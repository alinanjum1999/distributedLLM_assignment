from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model(model_name):
    if model_name == "llama2":
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
        model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    elif model_name == "mistral":
        tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
        model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
    else:
        raise ValueError("Unsupported model: {}".format(model_name))
    
    return tokenizer, model

def generate_response(model, query):
    tokenizer, model = model
    inputs = tokenizer(query, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
