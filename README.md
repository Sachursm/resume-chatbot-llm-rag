# Resume Chatbot — Local AI Resume Q&A Assistant

This project is an AI-powered Resume Chatbot that allows you to upload a resume and chat with it like ChatGPT — completely offline and private.
It uses FAISS Vector Search for retrieval and Mistral 7B GGUF running locally using llama-cpp-python.

---

## 💡 What It Can Do

Upload any resume PDF and ask questions like:
* Work experience summary
* Technologies and tools used
* Company names
* Skills in the resume
* Education details
* Or any custom question

**🎯 No Hallucinations:**
* If the information is not present, the bot does not hallucinate
* It clearly replies: "Not available in resume."

---

## ✨ Features

* 🧠 **Local AI Model** – No Internet Required
* 🔍 **FAISS-based semantic search**
* 📄 **PDF Resume Upload**
* 💬 **Interactive Chat UI**
* 🛢️ **Chat History + Resume Storage** using SQLite
* 🧰 **Rule-based extraction** for:
  * Name
  * Email
  * Phone
  * Skills
  * Company / Experience
* 🔐 **Privacy Safe** – Resume never leaves your machine

---

## 🏗️ Tech Stack

* **Backend:** Flask
* **AI Model:** Mistral 7B (GGUF) + llama-cpp-python
* **Vector DB:** FAISS
* **PDF Processing:** PyPDF
* **Database:** SQLite
* **Frontend:** HTML + CSS + JS

---

## 📥 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/resume-chatbot.git
cd resume-chatbot
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
```

**Activate the environment:**

* **Windows:**
```bash
  venv\Scripts\activate
```

* **Linux / Mac:**
```bash
  source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🤖 Model Setup

### ✅ Step 1: Download the Model

Download this recommended model (balanced speed + accuracy):

**Model:** `mistral-7b-instruct-v0.2.Q4_K_M.gguf`

You can get it from any of these sources:
* [HuggingFace - TheBloke](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
* [Alternative Mirror - MistralAI](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)

### 📂 Step 2: Place Model in Folder

Create folder:
```
C:/Users/<YourUserName>/Documents/llm_models/
```

Then place the model file inside:
```
C:/Users/<YourUserName>/Documents/llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

**Example final path:**
```
C:/Users/sachu/Documents/llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

### ⚙️ Step 3: Verify Model Path in Code

Open:
```
scripts/llm_mistral.py
```

Make sure this matches your model location:
```python
default_path = "C:/Users/sachu/Documents/llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
```

> **Note:** If you placed the model somewhere else — update the path.

### 🧠 Step 4: llama.cpp / llama-cpp-python Requirement

We use `llama-cpp-python`, which is already installed in `requirements.txt`.

If you missed installing it:
```bash
pip install llama-cpp-python
```

**📝 Windows users must have Visual Studio Build Tools installed:**
* Download: [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
* During install, select:
  * ✔ Desktop Development with C++
  * ✔ CMake

---

## 🚀 Running the Application

### 5️⃣ Start the App
```bash
python app.py
```

Then open in your browser:
```
http://127.0.0.1:5000
```

Upload a resume → Start chatting 🎉

---

## 🖼️ Screenshots


* `/screenshots/home.png`
  ![Home page](https://github.com/Sachursm/resume-chatbot-llm-rag/blob/d2038739b02218e49301d10e3876292ff1d57ed6/upload.png)
* `/screenshots/chat.png`
  ![Chat page](https://github.com/Sachursm/resume-chatbot-llm-rag/blob/1fb004bde65211e1ce58b7e61694b83a82e41959/chat.png)
---

## 📂 Project Structure
```
resume-chatbot/
│
├── app.py
├── database.db
├── requirements.txt
├── uploads/
├── templates/
│   ├── upload.html
│   └── chat.html
│
└── scripts/
    ├── llm_mistral.py
    ├── retriever.py
    ├── pdf_loader.py
    ├── chunking.py
    ├── extractors.py
    ├── db.py
    └── utils.py
```

---

## 🛠️ Troubleshooting

### ❌ llama-cpp-python installation fails on Windows

**Solution:**
1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Enable components:
   * Desktop Development with C++
   * C++ CMake Tools
   * Windows SDK
3. Then reinstall:
```bash
   pip install llama-cpp-python
```

### ❌ Model Not Loading?

**Check your model path:**
```python
model_path = "C:/Users/YourName/Documents/llm_models/mistral-7b-instruct.gguf"
```

### ❌ Chatbot Not Responding?

**Restart Flask:**
```bash
python app.py
```

**Also ensure:**
* Resume uploaded successfully
* Database was created

---

## 🧭 Roadmap / Future Improvements

- [ ] Support DOCX resume
- [ ] Add authentication
- [ ] Export chat history
- [ ] Deployable build
- [ ] GPU acceleration
- [ ] Web UI improvements
- [ ] AWS version

---

## 🤝 Contributing

Pull requests are welcome!  
For major changes, please open an issue first.

---

## 📜 License

This project is open-source.

---

## 👤 Author

**Sachu Retna S M**  
*AI & Robotics Developer*

---

## 🔗 Links

* [GitHub Repository](https://github.com/Sachursm/resume-chatbot-llm-rag.git)



