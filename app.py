from flask import Flask, render_template, request, redirect, jsonify
import os
from isort import file
from scripts.pdf_loader import load_pdf_text
from scripts.chunking import chunk_by_lines
from scripts.retriever import FaissRetriever
from scripts.llm_engine import LocalLLM
from scripts.utils import normalize_query
from scripts.extractors import extract_name, extract_email, extract_phone, extract_skills
from scripts.db import get_connection, init_db

chat_history = []
current_resume_name = ""

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
    global current_resume_name
    current_resume_name = file.filename
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
        data = request.get_json()
        query = data.get("question", "")
        query_norm = normalize_query(query)

        # Rule-based answers
        if "name" in query_norm:
            answer = extract_name(resume_text)

        elif "email" in query_norm:
            answer = extract_email(resume_text)

        elif "phone" in query_norm:
            answer = extract_phone(resume_text)

        elif "skill" in query_norm:
            skills = extract_skills(resume_text)
            answer = "\n".join(skills)

        else:
            context_chunks = retriever.retrieve(query_norm)
            if not context_chunks:
                answer = "I don't know based on the document."
            else:
                context = "\n".join(context_chunks)
                answer = llm.answer(context, query)

        chat_history.append({"user": query, "bot": answer})

        return jsonify({
            "answer": answer,
            "history": chat_history
        })

    return render_template(
        "chat.html",
        resume_name=current_resume_name
    )


if __name__ == "__main__":
    app.run(debug=True)
