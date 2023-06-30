import os
from flask import Flask, render_template, request, jsonify
from langchain import OpenAI
from chat import generate_response
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, PromptHelper, LLMPredictor
import openai

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.environ.get("OPENAI_API_KEY")
documents = SimpleDirectoryReader('./data').load_data()

app = Flask(__name__)

# Initialize prompt_helper and index
llm_predictor = None
prompt_helper = None
index = None

@app.route("/")
def index_get():
    script_root = request.script_root
    return render_template("index.html", script_root=script_root)

@app.route("/initialize")
def initialize():
    global llm_predictor, prompt_helper, index
    
    # Initialize llm_predictor
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.1, model_name="text-davinci-002"))

    # Initialize prompt_helper and index
    max_input_size = 4096
    num_output = 8
    max_chunk_overlap = 0.2
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
    index = GPTVectorStoreIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    
    # Store index in global scope
    globals()["index"] = index
    print("Index initialized")
    return "Initialization successful"

@app.post("/predict")
def predict():
    if index is None:
        return "Index not initialized. Please call the /initialize endpoint first."
    
    text = request.get_json().get("message")
    # Generate response
    response = generate_response(index, text.lower())
    message = {"answer" : response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
