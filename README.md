### Objective:

Develop a full-stack application enabling users to upload PDF documents and ask questions about their content. The backend processes PDFs and utilizes NLP to answer questions.

---

### Tools and Technologies:

- **Backend:** FastAPI
- **NLP Processing:** LangChain
- **Frontend:** React.js
- **Database:** MySQL
- **File Storage:** Local filesystem or AWS S3

---

### Functional Requirements:

#### 1. PDF Upload:

- Users can upload PDF documents.
- Store PDFs and optionally extract and save their text for processing.

#### 2. Asking Questions:

- Users can ask questions related to an uploaded PDF.
- Process the question and PDF content to generate answers.

#### 3. Displaying Answers:

- Show answers to user queries.
- Allow follow-up or new questions based on the same document.

---

### Non-Functional Requirements:

- **Usability:** Intuitive and user-friendly interface.
- **Performance:** Optimized PDF processing and question-answering speed.

---

### Backend Specification:

#### 1. FastAPI Endpoints:

- Upload PDF documents.
- Handle user questions and return relevant answers.

#### 2. PDF Processing:

- Extract text from PDFs using PyMuPDF.
- Utilize LangChain for NLP-based question answering.

#### 3. Data Management:

- Store document metadata (filename, upload date) in a MySQL database.

---

### Frontend Specification:

#### 1. User Interface:

- Upload PDFs.
- Ask questions and view answers.

#### 2. Interactivity:

- Feedback mechanisms during uploads and processing.
- Error messages for unsupported files or processing failures.

---

### Design:

- Refer to the design mockup for UI structure and layout: [Figma Design Link](https://www.figma.com/file/QHpASp7wGRRcjh0oxCuspL/FullStack-Engineer-Internship-Assignment?type=design\&node-id=0-1\&mode=design\&t=geu9rfpXEecN8eFZ-0)

---

### [Assignment Deliverables:](https://www.figma.com/file/QHpASp7wGRRcjh0oxCuspL/FullStack-Engineer-Internship-Assignment?type=design\&node-id=0-1\&mode=design\&t=geu9rfpXEecN8eFZ-0)

1. **Source Code:**

   - Backend and frontend codebase, structured and well-commented.

2. **Documentation:**

   - README file with setup instructions.
   - API documentation and application architecture overview.

### Evaluation Criteria:

- **Functionality:** Completeness of features.
- **Code Quality:** Clean, structured, and well-commented code.
- **Design and UX:** Ease of use and aesthetic appeal.
- **Innovation:** Extra features enhancing usability or performance.

---

### Steps to Run the Code:

1. **Backend Setup:**
   - Install dependencies:
     ```bash
     pip install fastapi sqlalchemy mysql-connector-python pymupdf langchain uvicorn
     ```
   - Create MySQL database:
     ```sql
     CREATE DATABASE pdf_db;
     ```
   - Update database URL in the code:
     ```python
     DATABASE_URL = "mysql+mysqlconnector://root:@localhost/pdf_db"
     ```
   - Run the backend:
     ```bash
     uvicorn main:app --reload
     ```

**Frontend Setup:**

- Navigate to frontend directory:
  ```bash
  cd frontend
  ```
- Install dependencies:
  ```bash
  npm install
  ```
- Start the frontend server:
  ```bash
  npm start
  ```

3. **Access the Application:**

   - Open browser and visit:
     ```
     http://localhost:3000
     ```

4. **Test the Application:**

   - Upload a PDF and ask questions about its content.
