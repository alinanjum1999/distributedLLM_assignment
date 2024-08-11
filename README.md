

# Distributed LLM Assignment



## Introduction

This project includes a Flask-based API server that allows users to interact with different language models, specifically Llama2 and Mistral, hosted on Hugging Face. The server supports selecting a model, sending queries, and maintaining conversation context.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8+**
- **Pip** (Python package installer)
- **Hugging Face API Token**: You will need an API token from Hugging Face to load protected models like Llama2 and Mistral.

## Project Structure

```
distributed-llm-assignment
├── python-llm
│   ├── app.py
│   ├── model_utils.py
│   ├── requirements.txt
├── README.md
```

## Environment Variables

The project requires a Hugging Face API token to access certain models. You should set this token as an environment variable:

### Setting the Environment Variable

- On **Windows** (Command Prompt):

  ```cmd
  set HUGGINGFACE_API_TOKEN=your_huggingface_api_token
  ```

- On **macOS/Linux**:

  ```bash
  export HUGGINGFACE_API_TOKEN=your_huggingface_api_token
  ```

Alternatively, you can create a `.env` file in the `python-llm` directory:

```env
HUGGINGFACE_API_TOKEN=your_huggingface_api_token
```

## Installation and Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/alinanjum1999/distributed-llm-assignment.git
   cd distributed-llm-assignment/python-llm
   ```

2. **Install Dependencies**:

   Make sure you have the required Python packages installed:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:

   Ensure the Hugging Face API token is set as described in the [Environment Variables](#environment-variables) section.

## Running the Application

To start the Flask API server, navigate to the `python-llm` directory and run:

```bash
python app.py
```

### Expected Output

If everything is set up correctly, you should see something like this in your terminal:

```bash
* Serving Flask app 'app'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

This indicates that the server is running and ready to accept requests on port `5000`.

## API Endpoints

### 1. Select Model

**POST** `/select-model`

- **Description**: Select a model (Llama2 or Mistral) to interact with.
- **Request Body**:

  ```json
  {
    "model": "llama2"
  }
  ```

- **Response**:

  ```json
  {
    "conversation_id": "1"
  }
  ```

- **Error Response**:

  ```json
  {
    "error": "Error loading model llama2: [Error details here]"
  }
  ```

### 2. Query Model

**POST** `/query`

- **Description**: Send a query to the selected model.
- **Request Body**:

  ```json
  {
    "conversation_id": "1",
    "query": "What is the capital of France?"
  }
  ```

- **Response**:

  ```json
  {
    "response": "The capital of France is Paris.",
    "conversation_id": "1"
  }
  ```

- **Error Response**:

  ```json
  {
    "error": "Invalid conversation ID"
  }
  ```

## Troubleshooting

If the application doesn't behave as expected, here are some steps to help diagnose and fix common issues:

### 1. **Environment Variables Not Set**

Make sure the `HUGGINGFACE_API_TOKEN` is correctly set. You can check by printing the environment variable:

```python
import os
print(os.getenv('HUGGINGFACE_API_TOKEN'))
```

### 2. **Server Doesn't Start**

If the server doesn't start or you see an error:

- Check the console output for error messages.
- Ensure all dependencies are installed.
- Confirm that port `5000` is not in use by another application.

### 3. **Model Fails to Load**

If the model fails to load:

- Verify that the model name is correct (`llama2` or `mistral`).
- Ensure your Hugging Face API token has the necessary permissions.

## License

This project is licensed under the MIT License.
```

This `README.md` should now provide clear guidance on setting up and running the Flask API, interacting with the models, and troubleshooting common issues.
