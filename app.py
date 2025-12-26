from flask import Flask, render_template, request, redirect, jsonify
import os

from scripts.pdf_loader import load_pdf_text
from scripts.chunking import chunk_by_lines
from scripts.retriever import FaissRetriever
from scripts.llm_engine import LocalLLM
from scripts.utils import normalize_query
from scripts.extractors import *
from scripts.db import *

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

llm = LocalLLM()
retriever = None
resume_text = ""


@app.route("/", methods=["GET", "POST"])
def upload():
    global retriever, resume_text

    if request.method == "POST":
        file = request.files["resume"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        resume_text = load_pdf_text(path)
        chunks = chunk_by_lines(resume_text)
        retriever = FaissRetriever(chunks)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO resumes(filename,text) VALUES (?,?)",
                    (file.filename, resume_text))
        resume_id = cur.lastrowid
        conn.commit()
        conn.close()

        return redirect(f"/chat/{resume_id}")

    return render_template("upload.html", resumes=get_all_resumes())


@app.route("/chat/<int:resume_id>", methods=["GET", "POST"])
def chat(resume_id):
    global resume_text, retriever

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT filename,text FROM resumes WHERE id=?", (resume_id,))
    row = cur.fetchone()
    conn.close()

    resume_name = row[0]
    resume_text = row[1]

    chunks = chunk_by_lines(resume_text)
    retriever = FaissRetriever(chunks)

    if request.method == "POST":
        data = request.get_json()
        q = data["question"]
        qn = normalize_query(q)

        if "name" in qn:
            answer = extract_name(resume_text)
        elif "email" in qn:
            answer = extract_email(resume_text)
        elif "phone" in qn:
            answer = extract_phone(resume_text)
        elif "skill" in qn:
            answer = ", ".join(extract_skills(resume_text))
        else:
            ctx = "\n".join(retriever.retrieve(q))
            answer = llm.answer(ctx, q)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_history(resume_id,question,answer) VALUES (?,?,?)",
            (resume_id, q, answer)
        )
        conn.commit()
        conn.close()

        return jsonify({"answer": answer})

    return render_template("chat.html", resume_name=resume_name, resume_id=resume_id)


if __name__ == "__main__":
    app.run(debug=True)
