# Local LLM Wrapper
from transformers import pipeline

class LocalLLM:
    def __init__(self):
        self.llm = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=0
        )

    def answer(self, context: str, query: str) -> str:
        prompt = f"""
You are a helpful assistant answering questions about a resume.

Use ONLY the information provided below.
If not present, say:
"I don't know based on the document."

Context:
{context}

Question:
{query}

Answer:
"""
        result = self.llm(prompt, max_length=500)
        return result[0]["generated_text"]
