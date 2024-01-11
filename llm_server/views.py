from flask import render_template, request, send_from_directory

from llm_server import app
from .rag import RagLLM, RetrievalClassifier

retrieval_classifier = RetrievalClassifier()
rag_llm = RagLLM(retrieval_classifier)


@app.route('/response', methods=['POST'])
def respond():
    text = request.json['text']
    response = rag_llm.get_response(text)
    return {"response": response}


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('build', path)
