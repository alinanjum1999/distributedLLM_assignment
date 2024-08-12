
# Distributed LLM Assignment

## Overview

This project demonstrates a distributed system where a Node.js backend communicates with a Python-based Language Model (LLM) service. The Python service loads pre-trained models and processes queries sent from the backend. The models are preloaded and saved to disk to reduce load times during runtime. However, please note that loading these models can still take some time, especially on systems with limited resources.

**Important Note**: Even on a computer with 16GB of RAM, loading large models like Llama2 or Mistral can take significant time and may temporarily consume a large amount of system memory. It's crucial to monitor system resources and be patient while the model is loading.

## Setup Instructions

### Prerequisites

- **Docker**: Ensure Docker and Docker Compose are installed on your system.
- **Python**: Required for running the Python LLM service and preloading models.
- **Node.js**: Required for the backend API server.
- **Insomnia**: Required for testing the API endpoints.

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/distributed-llm-assignment.git
cd distributed-llm-assignment
```

### Step 2: Set Up Environment Variables

Create a `.env` file in both the `python-llm` and `backend` directories with the following content:

```env
HUGGINGFACE_API_TOKEN=your_huggingface_api_token
```

Replace `your_huggingface_api_token` with your actual Hugging Face API token.

### Step 3: Preload Models

Before running the services, preload the models:

```bash
cd python-llm
python preload_models.py
```

This script will download the models from Hugging Face and save them in the `preloaded_models` directory. This step may take a while depending on your internet connection and the size of the models.

### Step 4: Run the Services with Docker Compose

Navigate back to the root directory and run the Docker Compose setup:

```bash
docker-compose up --build
```

This command builds and runs the services in Docker containers. The Python service will load the preloaded models and the Node.js backend will be ready to accept API requests.

### Step 5: Setting Up Insomnia

Insomnia is an API testing tool that allows you to send requests to your backend and test the endpoints.

1. **Download and Install Insomnia**: [Insomnia Download](https://insomnia.rest/download)
2. **Create a New Request Collection**: Open Insomnia and create a new request collection for your project.
3. **Add a Request to Select a Model**:
    - **Request Name**: Select Model
    - **Method**: POST
    - **URL**: `http://localhost:3000/api/select-model`
    - **Body**: 
    ```json
    {
      "model": "model_name"
    }
    ```
    Replace `"model_name"` with the model you want to load (e.g., `"llama2"`).

4. **Add a Request to Query the Model**:
    - **Request Name**: Query Model
    - **Method**: POST
    - **URL**: `http://localhost:3000/api/query`
    - **Body**: 
    ```json
    {
      "conversation_id": "conversation_id_value",
      "query": "Your question here"
    }
    ```
    Replace `"conversation_id_value"` with the conversation ID returned from the `Select Model` request and `"Your question here"` with your query.

### Step 6: Testing the API

1. **Select a Model**: First, send a request to the `Select Model` endpoint to load a model. The model might take some time to load, especially large models like Llama2 or Mistral. Be patient as the backend processes this request.

2. **Send a Query**: Once the model is loaded and you have a conversation ID, you can send queries to the model using the `Query Model` endpoint. The response should return a generated answer from the model.

### Expected Output

- **Model Selection**: A successful response will return a `conversation_id` which you will use in subsequent queries.
- **Querying the Model**: A successful response will include the model's generated text in the `response` field.

### Troubleshooting

- **Long Loading Times**: Be aware that loading large models on systems with 16GB RAM or less may take several minutes. Ensure your system has enough memory and consider increasing swap space if needed.
- **Memory Issues**: If you encounter memory-related errors, consider using a smaller model or running the services on a system with more RAM.

### Conclusion

This project demonstrates a distributed system where a Node.js backend interacts with a Python-based LLM service. The system is designed to handle large models by preloading them and making them available for efficient querying. While the setup is resource-intensive, it showcases how to manage and utilize large-scale language models in a distributed environment.

For any further assistance or issues, please feel free to reach out 


