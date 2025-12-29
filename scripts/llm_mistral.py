# scripts/llm_mistral.py

from llama_cpp import Llama
import re


class LocalLLM:
    def __init__(self, model_path: str = None):
        default_path = "C:/Users/sachu/Documents/llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

        self.llm = Llama(
            model_path=model_path or default_path,
            n_ctx=4096,
            n_threads=6,
            n_gpu_layers=0,       # Change to >0 if GPU
            verbose=False
        )

        self.cache = {}

    # -------------------- UTILITIES -------------------- #
    def _clean(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text).strip()
        return text.replace("</s>", "").strip()

    def _prompt(self, context: str, question: str) -> str:
        return f"""
<s>[INST]
You are a Resume Q&A Assistant.

RULES:
- Use ONLY information inside RESUME.
- Do NOT guess or assume.
- If answer is missing, reply EXACTLY: Not available in resume.
- Be clear, factual and complete.

RESUME:
{context}

QUESTION:
{question}

Answer:
[/INST]
"""

    # -------------------- MAIN ANSWER FUNCTION -------------------- #
    def answer(self, context: str, question: str, use_cache=True) -> str:
        key = f"{hash(context)}_{hash(question)}"
        if use_cache and key in self.cache:
            return self.cache[key]

        prompt = self._prompt(context, question)

        response = self.llm(
            prompt,
            max_tokens=500,
            temperature=0.1,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.15,
            stop=["</s>"],
            echo=False
        )

        answer = self._clean(response["choices"][0]["text"])

        # Safety fallback
        if answer.strip() == "":
            answer = "Not available in resume."

        if use_cache:
            self.cache[key] = answer

        return answer

    # optional helper if needed later
    def clear_cache(self):
        self.cache.clear()



