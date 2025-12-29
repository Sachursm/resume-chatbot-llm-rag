# scripts/llm_mistral.py

from llama_cpp import Llama


class LocalLLM:
    def __init__(self):
        self.llm = Llama(
            model_path="C:/Users/sachu/Documents/llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            n_ctx=4096,
            n_threads=6
        )

    def answer(self, context: str, query: str) -> str:
        prompt = f"""
You are a Resume QA Assistant.

ONLY answer using the text inside RESUME.
DO NOT guess. 
If answer is missing, say: "Not available in resume."

--------------------
RESUME:
{context}
--------------------

Question: {query}

Provide a clear answer:
"""


        response = self.llm(
            prompt,
            max_tokens=400,
            temperature=0.1,
            top_p=0.9,
            do_sample=False,
            stop=["Question:", "Resume:"]
        )

        return response["choices"][0]["text"].strip()
