# 🤖 AI-Powered RAG Document Assistant

An **AI-powered document question-answering system** built using **Retrieval-Augmented Generation (RAG)**. The application allows users to upload PDF or TXT documents and ask questions about their content.

Instead of relying on general knowledge, the system retrieves relevant information from the uploaded document and uses a local **Llama 3.2** model through **Ollama** to generate an accurate, context-based answer.

---

## 🚀 Features

* 📄 Upload **PDF and TXT** documents
* ✂️ Automatically split documents into smaller text chunks
* 🔎 Semantic similarity search using **FAISS**
* 🧠 Generate embeddings for document chunks
* 🤖 Local AI response generation using **Llama 3.2**
* 💬 Ask natural-language questions about uploaded documents
* 🎯 Uses only relevant document context to generate answers
* 🛡️ Prevents answers based on outside knowledge when information is unavailable
* 📚 Returns the retrieved source chunks along with the answer
* 🌐 Simple web-based frontend
* ⚡ FastAPI backend for handling document processing and queries

---

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation pipeline:

```text
              ┌─────────────────┐
              │  Upload PDF/TXT │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │  Text Extraction│
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │  Text Chunking  │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │   Embeddings    │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │  FAISS Vector DB│
              └────────┬────────┘
                       │
                       │ User Question
                       ↓
              ┌─────────────────┐
              │ Similarity Search│
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Relevant Context│
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │   Llama 3.2     │
              │    via Ollama   │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │      Answer     │
              └─────────────────┘
```

### RAG Pipeline

1. **Document Upload**
   The user uploads a PDF or TXT document.

2. **Text Extraction**
   Text is extracted from the uploaded file.

3. **Chunking**
   The extracted text is divided into smaller overlapping chunks.

4. **Embedding Generation**
   The chunks are converted into vector representations.

5. **Vector Database**
   The embeddings are stored and searched using FAISS.

6. **Question Processing**
   When the user asks a question, the system searches for the most relevant document chunks.

7. **Context Creation**
   The retrieved chunks are combined to create relevant context.

8. **AI Generation**
   The context and question are sent to the local Llama 3.2 model through Ollama.

9. **Answer Generation**
   The model generates an answer using the retrieved document information.

---

## 🛠️ Technologies Used

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| **Python**     | Backend development         |
| **FastAPI**    | REST API and backend server |
| **PyPDF2**     | PDF text extraction         |
| **FAISS**      | Vector similarity search    |
| **Ollama**     | Local LLM execution         |
| **Llama 3.2**  | Question-answering model    |
| **HTML**       | Frontend structure          |
| **CSS**        | Frontend styling            |
| **JavaScript** | Frontend interaction        |

---

## 📂 Project Structure

```text
AI-Powered-RAG-Document-Assistant/
│
├── index.html       # Frontend interface
├── style.css        # Frontend styling
├── script.js        # Frontend JavaScript
│
├── main.py          # FastAPI backend
├── rag.py           # RAG pipeline and vector search
│
└── README.md        # Project documentation
```

---

## ⚙️ Requirements

Before running the project, make sure you have:

* Python 3.9+
* Ollama
* Llama 3.2 model
* Required Python packages

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/swastikgit1234/AI-Powered-RAG-Document-Assistant.git
```

```bash
cd AI-Powered-RAG-Document-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn python-multipart pydantic PyPDF2 requests faiss-cpu sentence-transformers
```

---

## 🦙 Set Up Ollama

Install Ollama and make sure it is running on your computer.

Then download the Llama 3.2 model:

```bash
ollama pull llama3.2
```

The backend communicates with Ollama through its local API.

The project currently sends generation requests to:

```text
http://localhost:11434/api/generate
```

and uses the `llama3.2` model.

---

## ▶️ Run the Application

Start the FastAPI backend:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Open the frontend:

```text
index.html
```

in your browser.

---

## 📄 Supported Documents

Currently supported:

* `.pdf`
* `.txt`

The backend rejects unsupported file types.

---

## 🔌 API Endpoints

### `GET /`

Checks whether the RAG API is running.

Example response:

```json
{
  "message": "RAG Document Assistant API is running."
}
```

### `POST /upload`

Uploads a PDF or TXT document and processes it.

The document is:

```text
Uploaded
   ↓
Text Extracted
   ↓
Split into Chunks
   ↓
Embeddings Created
   ↓
FAISS Database
```

### `POST /ask`

Accepts a question and searches the vector database for relevant information.

Example request:

```json
{
  "question": "What is the main topic of this document?"
}
```

The system retrieves the most relevant chunks and sends them as context to Llama 3.2.

---

## 🎯 Hallucination Control

One of the important features of this project is that the AI is instructed to answer **only from the retrieved document context**.

If the required information cannot be found, the system returns:

```text
Information was not found in the uploaded document.
```

A similarity threshold is also applied before generating the response, helping prevent irrelevant document content from being used.

---

## 💡 Example Use Case

Imagine you upload a college syllabus:

```text
college_syllabus.pdf
```

You can ask:

```text
What subjects are included in the 4th semester?
```

The system:

```text
Question
   ↓
FAISS Similarity Search
   ↓
Relevant syllabus chunks
   ↓
Llama 3.2
   ↓
Answer
```

This makes the application useful for interacting with:

* 📚 Study materials
* 📑 Research papers
* 📖 Books and notes
* 📝 Reports
* 📄 Documentation
* 🎓 Academic documents

---

## 🔐 Privacy

The project uses **Ollama locally** for Llama 3.2 inference. This allows the language model to run on the user's own machine rather than requiring a cloud-based LLM API.

---

## 🔮 Future Improvements

Possible future enhancements include:

* Support for DOCX files
* Multiple-document conversations
* Conversation history
* Improved document parsing
* Streaming AI responses
* Source citation highlighting
* Better chunking strategies
* Metadata filtering
* Persistent vector databases
* Authentication and user accounts
* Deployment to a cloud platform

---

## 👨‍💻 Author

**Swastik Das**

GitHub:
https://github.com/swastikgit1234

Project Repository:
https://github.com/swastikgit1234/AI-Powered-RAG-Document-Assistant

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**AI-Powered RAG Document Assistant** — making document interaction smarter with Retrieval-Augmented Generation.

