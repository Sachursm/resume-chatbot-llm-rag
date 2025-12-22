# TERMINAL CHATBOT (MAIN FILE)

from scripts.pdf_loader import load_pdf_text
from scripts.chunking import chunk_by_lines
from scripts.retriever import FaissRetriever
from scripts.extractors import extract_name, extract_email, extract_phone, extract_skills
from scripts.llm_engine import LocalLLM
from scripts.utils import normalize_query

PDF_PATH = "data/SACHU RETNA S M.pdf"

def main():
    text = load_pdf_text(PDF_PATH)
    chunks = chunk_by_lines(text)

    retriever = FaissRetriever(chunks)
    llm = LocalLLM()

    print("\n🤖 Resume Chatbot Ready")
    print("Type 'exit' to quit\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break

        query = normalize_query(query)

        # Rule-based answers
        if "name" in query:
            print("Bot:", extract_name(text))
            continue

        if "email" in query:
            print("Bot:", extract_email(text))
            continue

        if "phone" in query:
            print("Bot:", extract_phone(text))
            continue

        if "skill" in query:
            skills = extract_skills(text)
            print("Bot: Key skills include:")
            for s in skills:
                print("-", s)
            continue

        # RAG retrieval
        context_chunks = retriever.retrieve(query)

        if not context_chunks:
            print("Bot: I don't know based on the document.")
            continue

        context = "\n".join(context_chunks)
        answer = llm.answer(context, query)
        print("Bot:", answer)


if __name__ == "__main__":
    main()

