from flask import Flask, render_template, request, redirect
import os

from scripts.pdf_loader import load_pdf_text
from scripts.chunking import chunk_by_lines
from scripts.retriever import FaissRetriever
from scripts.llm_engine import LocalLLM
from scripts.utils import normalize_query
from scripts.extractors import extract_name, extract_email, extract_phone, extract_skills

from db import get_connection, init_db

UPLOAD_FOLDER = "data/uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

init_db()

# Global objects (simple for now)
retriever = None
llm = LocalLLM()
resume_text = ""

@app.route("/", methods=["GET", "POST"])
def upload():
    global retriever, resume_text

    if request.method == "POST":
        file = request.files["resume"]
        if not file:
            return "No file uploaded"

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        resume_text = load_pdf_text(path)
        chunks = chunk_by_lines(resume_text)
        retriever = FaissRetriever(chunks)

        # Save to DB
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO resumes (filename, text) VALUES (?, ?)",
            (file.filename, resume_text)
        )
        conn.commit()
        conn.close()

        return redirect("/chat")

    return render_template("upload.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        query = request.form["question"]
        query_norm = normalize_query(query)

        # Rule-based
        if "name" in query_norm:
            return extract_name(resume_text)

        if "email" in query_norm:
            return extract_email(resume_text)

        if "phone" in query_norm:
            return extract_phone(resume_text)

        if "skill" in query_norm:
            skills = extract_skills(resume_text)
            return "<br>".join(skills)

        # RAG
        context_chunks = retriever.retrieve(query_norm)

        if not context_chunks:
            return "I don't know based on the document."

        context = "\n".join(context_chunks)
        answer = llm.answer(context, query)

        return answer

    return render_template("chat.html")


if __name__ == "__main__":
    app.run(debug=True)
