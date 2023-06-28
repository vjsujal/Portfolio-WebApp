import os
from flask import Flask, render_template, request, jsonify
from langchain import OpenAI
from chat import generate_response
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, PromptHelper, LLMPredictor
import openai


os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"
documents = SimpleDirectoryReader('./data').load_data()

# define LLM
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.1, model_name="text-davinci-002"))

# define prompt helper
# set maximum input size
max_input_size = 4096
# set number of output tokens
num_output = 8
# set maximum chunk overlap
max_chunk_overlap = 0.2
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

index = GPTVectorStoreIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

app = Flask(__name__)

@app.route("/")
def index_get():
    script_root = request.script_root
    return render_template("index.html", script_root=script_root)

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check text is valid
    response = generate_response(index,text.lower())
    message = {"answer" : response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
    


