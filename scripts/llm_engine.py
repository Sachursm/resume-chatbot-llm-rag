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
You are a resume assistant.
Answer ONLY using the provided resume context.
If not in resume, say "Not available in resume".


Resume Context:
{context}


Context:
{context}

Question:
{query}

Answer:
"""
        result = self.llm(prompt, max_length=500)
        return result[0]["generated_text"]
