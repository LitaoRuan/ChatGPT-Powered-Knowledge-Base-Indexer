from flask import Flask, render_template, request, jsonify
from rag_core import search_chunks, ask_with_context

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    top_chunks = search_chunks(question, top_k=5)
    answer = ask_with_context(question, top_chunks)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
