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


# @app.route("/chat/<int:resume_id>", methods=["GET", "POST"])
# def chat(resume_id):
#     global resume_text, retriever

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT filename,text FROM resumes WHERE id=?", (resume_id,))
#     row = cur.fetchone()
#     conn.close()

#     resume_name = row[0]
#     resume_text = row[1]

#     chunks = chunk_by_lines(resume_text)
#     retriever = FaissRetriever(chunks)

#     if request.method == "POST":
#         data = request.get_json()
#         q = data["question"]
#         qn = normalize_query(q)

#         if "name" in qn:
#             answer = extract_name(resume_text)
#         elif "email" in qn:
#             answer = extract_email(resume_text)
#         elif "phone" in qn:
#             answer = extract_phone(resume_text)
#         elif "skill" in qn:
#             answer = ", ".join(extract_skills(resume_text))
#         elif "company" in qn or "experience" in qn:
#             answer = extract_company(resume_text)


#         else:
#             ctx = "\n".join(retriever.retrieve(q))
#             answer = llm.answer(ctx, q)

#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO chat_history(resume_id,question,answer) VALUES (?,?,?)",
#             (resume_id, q, answer)
#         )
#         conn.commit()
#         conn.close()

#         return jsonify({"answer": answer})

#     return render_template("chat.html", resume_name=resume_name, resume_id=resume_id)
# try the new chat route below
@app.route("/chat/<int:resume_id>", methods=["GET", "POST"])
def chat(resume_id):
    conn = get_connection()
    cur = conn.cursor()

    # Load resume
    cur.execute("SELECT filename, text FROM resumes WHERE id=?", (resume_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Resume not found", 404

    filename = row[0]
    resume_text = row[1]

    # Build retriever everytime user enters chat page
    chunks = chunk_by_lines(resume_text)
    retriever = FaissRetriever(chunks)

    # ---------------- POST -> Answer Question ----------------
    if request.method == "POST":
        data = request.get_json()
        question = data.get("question", "").strip()

        if question == "":
            conn.close()
            return jsonify({"answer": "Please ask something."})

        q = normalize_query(question)

        # RULE BASED ANSWERS
        if "name" in q:
            answer = extract_name(resume_text)

        elif "email" in q:
            answer = extract_email(resume_text)

        elif "phone" in q:
            answer = extract_phone(resume_text)

        elif "skill" in q:
            skills = extract_skills(resume_text)
            answer = "\n".join(skills) if skills else "No skills found"
        elif ("company" in q 
            or "experience" in q 
            or "company name" in q 
            or "previous work" in q 
            or "work experience" in q):
            answer = extract_company(resume_text)
                
        else:
            context = retriever.retrieve(q)

            if not context:
                answer = "I don't know based on the document."
            else:
                answer = llm.answer("\n".join(context), question)

        # SAVE CHAT TO DATABASE
        cur.execute(
            "INSERT INTO chat_history(resume_id, question, answer) VALUES (?, ?, ?)",
            (resume_id, question, answer)
        )
        conn.commit()
        conn.close()

        return jsonify({"answer": answer})

    # ---------------- GET -> Load Chat History ----------------
    cur.execute(
        "SELECT question, answer FROM chat_history WHERE resume_id=? ORDER BY id ASC",
        (resume_id,)
    )
    history_rows = cur.fetchall()
    conn.close()

    chat_history = [{"user": r[0], "bot": r[1]} for r in history_rows]

    return render_template(
        "chat.html",
        resume_id=resume_id,
        resume_name=filename,
        chat_history=chat_history
    )

@app.route("/delete/<int:resume_id>")
def delete_resume(resume_id):
    conn = get_connection()
    cur = conn.cursor()

    # delete chat history first (FK safety)
    cur.execute("DELETE FROM chat_history WHERE resume_id = ?", (resume_id,))

    # delete resume
    cur.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
