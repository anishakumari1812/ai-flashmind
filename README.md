# 🧠 FlashMind AI – AI Flashcard Generator

A production-ready Streamlit web application that turns your notes or PDFs into smart study flashcards using OpenAI's GPT API.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 Authentication | Login & Signup with SQLite + SHA-256 hashed passwords |
| 📝 Text Input | Paste study notes directly |
| 📄 PDF Upload | Auto-extract text from any PDF |
| 🤖 AI Flashcards | GPT-3.5-turbo generates 5–10 Q&A pairs |
| 💡 Card UI | Clean card layout with reveal-answer expanders |
| 🎨 Green Theme | Soft pastel green design system |
| 🚪 Session Management | Login/logout with `st.session_state` |

---

## 📂 Project Structure

```
flashmind-ai/
│
├── app.py                  # Entry point & page router
├── auth.py                 # Login / Signup UI
├── database.py             # SQLite user management
│
├── utils/
│   ├── llm.py              # OpenAI flashcard generation
│   └── pdf_reader.py       # PDF text extraction
│
├── pages/
│   ├── home.py             # Home page (input)
│   └── flashcards.py       # Flashcard display page
│
├── .streamlit/
│   └── config.toml         # Theme configuration
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & install dependencies

```bash
git clone <your-repo>
cd flashmind-ai
pip install -r requirements.txt
```

### 2. Set your OpenAI API key

```bash
# macOS / Linux
export OPENAI_API_KEY="sk-your-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY = "sk-your-key-here"
```

> **No API key?** The app runs in **Demo Mode** with sample flashcards — great for testing the UI!

### 3. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔐 Authentication

- Passwords are hashed with **SHA-256** before storage
- User data is stored in a local **SQLite** database (`flashmind.db`)
- Sessions persist via `st.session_state`

---

## 🤖 AI Integration

`utils/llm.py` → `generate_flashcards(text)`:

1. Sends study text to **GPT-3.5-turbo**
2. Receives a JSON array of `{"question": "...", "answer": "..."}` pairs
3. Validates & parses the response
4. Returns 5–10 flashcard dicts

Falls back to demo cards gracefully when no API key is set.

---

## 🎨 Theme

```toml
[theme]
primaryColor         = "#4CAF50"
backgroundColor      = "#F9FBF9"
secondaryBackgroundColor = "#E8F5E9"
textColor            = "#1B1B1B"
```

---

## 📦 Dependencies

```
streamlit>=1.32.0
openai>=1.12.0
pdfplumber>=0.10.3
```

---

## 🌐 Deployment

### Streamlit Community Cloud

1. Push your code to GitHub (add `OPENAI_API_KEY` as a **Secret** in the app settings)
2. Connect your repo at [share.streamlit.io](https://share.streamlit.io)
3. Set the main file to `app.py`

---

Built with ❤️ using Streamlit + OpenAI · Resume-ready project
