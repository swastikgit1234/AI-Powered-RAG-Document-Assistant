import os
import shutil
import requests

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from PyPDF2 import PdfReader

from rag import split_text, create_vector_database, search_similar_chunks


app = FastAPI(
    title="AI-Powered RAG Document Assistant"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str


# --------------------------------------------------
# Extract text from TXT
# --------------------------------------------------

def extract_txt(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        return file.read()


# --------------------------------------------------
# Extract text from PDF
# --------------------------------------------------

def extract_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# --------------------------------------------------
# Upload endpoint
# --------------------------------------------------

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    filename = file.filename

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    extension = os.path.splitext(filename)[1].lower()

    if extension not in [".pdf", ".txt"]:

        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed."
        )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract text
    if extension == ".pdf":

        text = extract_pdf(file_path)

    else:

        text = extract_txt(file_path)

    if not text.strip():

        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the document."
        )

    # Split into chunks
    chunks = split_text(
        text,
        chunk_size=800,
        overlap=150
    )

    # Create embeddings and FAISS database
    number_of_chunks = create_vector_database(chunks)

    return {
        "message": "Document uploaded successfully.",
        "filename": filename,
        "chunks": number_of_chunks
    }


# --------------------------------------------------
# Ask question endpoint
# --------------------------------------------------

@app.post("/ask")
async def ask_question(
    request: QuestionRequest
):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Search relevant chunks
    results = search_similar_chunks(
        question,
        top_k=4
    )

    if not results:

        return {
            "answer": "Information was not found in the uploaded document."
        }

    # --------------------------------------------------
    # Similarity threshold
    # --------------------------------------------------

    best_score = results[0]["score"]

    if best_score < 0.25:

        return {
            "answer": "Information was not found in the uploaded document."
        }

    # --------------------------------------------------
    # Create context
    # --------------------------------------------------

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    # --------------------------------------------------
    # Prompt Llama
    # --------------------------------------------------

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question ONLY using the information
provided in the CONTEXT below.

If the answer is not present in the context, say exactly:

"Information was not found in the uploaded document."

Do not use outside knowledge.
Do not make up information.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

    except requests.exceptions.ConnectionError:

        raise HTTPException(
            status_code=500,
            detail="Ollama is not running. Start Ollama first."
        )

    if response.status_code != 200:

        raise HTTPException(
            status_code=500,
            detail="Error communicating with Ollama."
        )

    data = response.json()

    answer = data.get(
        "response",
        "Information was not found in the uploaded document."
    )

    return {
        "answer": answer,
        "sources": [
            {
                "score": result["score"],
                "text": result["text"]
            }
            for result in results
        ]
    }


# --------------------------------------------------
# Home/test endpoint
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "RAG Document Assistant API is running."
    }