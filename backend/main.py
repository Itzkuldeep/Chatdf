from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import fitz  # PyMuPDF
import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Configuration
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/pdf_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), index=True)
    size = Column(Integer)
    num_pages = Column(Integer)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    db = SessionLocal()
    uploaded_files_info = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Save PDF
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Extract PDF metadata
        pdf_doc = fitz.open(file_path)
        num_pages = pdf_doc.page_count
        size = os.path.getsize(file_path)  # Get file size

        # Store metadata in DB
        db_document = Document(filename=file.filename, size=size, num_pages=num_pages)
        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        uploaded_files_info.append({
            "filename": file.filename,
            "message": "File uploaded successfully",
            "document_id": db_document.id,
            "size": size,
            "num_pages": num_pages
        })

    db.close()
    return {"uploaded_files": uploaded_files_info}

class Question(BaseModel):
    question: str

@app.post("/ask/")
async def ask_question(data: Question):
    db = SessionLocal()
    documents = db.query(Document).all()
    db.close()

    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")

    # Process text with LangChain and Google Generative AI
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = []
    metadata = []

    for document in documents:
        file_path = os.path.join(UPLOAD_DIR, document.filename)
        pdf_doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in pdf_doc)

        splits = text_splitter.split_text(text)
        all_splits.extend(splits)
        metadata.extend([{"source": document.filename}] * len(splits))

    # Create embeddings with metadata
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_texts(all_splits, embedding, metadatas=metadata)

    # Perform similarity search
    results = vectorstore.similarity_search_with_score(data.question, k=1)
    if results:
        answer = results[0][0].page_content
        source = results[0][0].metadata['source']  # Use metadata to get source
    else:
        answer = "No relevant answer found."
        source = "None"

    return {"answer": answer, "source": source}