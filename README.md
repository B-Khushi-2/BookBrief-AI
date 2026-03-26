# 📚 BookBrief AI

> ✨ _“Turn lengthy documents into powerful insights in seconds.”_

BookBrief AI is an **AI-powered document summarization platform** that automates the process of extracting key insights from PDF and text files using a seamless workflow of **Flask, n8n, Google Drive, and LLMs**.

---

## 🚀 Features

- 📄 Upload PDF / TXT files through a clean UI
- ⚡ Automated processing using n8n workflows
- 🤖 AI-generated structured summaries
- ☁️ Google Drive integration (input/output folders)
- 📥 Download summaries instantly
- 🕒 History tracking with delete options
- 🎯 Real-time summary display

---

## 🛠️ Tech Stack

| Layer         | Technology            |
| ------------- | --------------------- |
| Frontend      | HTML, CSS, JavaScript |
| Backend       | Python (Flask)        |
| Automation    | n8n                   |
| AI Model      | Groq (LLaMA 3)        |
| Cloud Storage | Google Drive API      |

---

## ⚙️ How It Works

```
User Upload → Flask Server → Google Drive (Input)
→ n8n Trigger → AI Processing → Output Folder
→ Flask Fetch → UI Display
```

---

## 📂 Project Structure

```
BookBrief-AI/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
│
├── n8n/
│   └── workflow.json
```

---

## 🧪 Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/BookBrief-AI.git
cd BookBrief-AI
```

---

### 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Configure environment

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 5️⃣ Run Flask app

```
python app.py
```

---

### 6️⃣ Setup n8n Workflow

1. Open n8n
2. Import `n8n/workflow.json`
3. Add credentials:
   - Google Drive
   - Groq API

4. Activate workflow

---

## 🔐 Security Note

Sensitive files like:

- `.env`
- `credentials.json`
- `token.pickle`

are excluded using `.gitignore`.

---

## 💡 Use Cases

- 📘 Book summarization
- 📄 Resume analysis
- 🧠 Quick learning from long documents
- 📊 Research content extraction

---

## 🧠 Key Highlights

- Modular architecture (UI + Backend + Automation)
- Real-time workflow execution
- Clean and user-friendly interface
- Scalable and cloud-integrated design

---

## 🎯 Future Improvements

- 🌐 Deploy on cloud (Render / AWS)
- 📱 Mobile-friendly UI
- 📊 Dashboard for analytics
- 🗣️ Voice-based summarization

---

## 👩‍💻 Author

**Khushi Borde**
CSE Student | AIML Enthusiast

---

## ⭐ Show Your Support

If you like this project, give it a ⭐ on GitHub!

---
