from flask import Flask, request, jsonify

app = Flask(__name__)

def generate_response(model, query):
    # This function would interact with the model to generate a response.
    # This is a mock implementation; replace it with actual model inference.
    return f"Response from {model} for query: {query}"

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    model = data.get('model')
    query = data.get('query')

    if not model or not query:
        return jsonify({"error": "Model and query are required."}), 400

    response = generate_response(model, query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
