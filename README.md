# Enterprise Knowledge Assistant

A Streamlit-based retrieval-augmented generation (RAG) app for asking questions about internal enterprise documents. It indexes PDF files into a local ChromaDB vector store, finds the most relevant sections for each question, and uses Google Gemini to produce a concise answer with its source sections.

## Features

- Ingests PDFs from a local `documents/` folder
- Splits documents into numbered sections and preserves source metadata
- Creates semantic embeddings with `BAAI/bge-small-en-v1.5`
- Stores and searches embeddings locally with ChromaDB
- Generates grounded answers with Gemini
- Shows the document and section used for each answer

## How it works

```text
PDFs in documents/ → text extraction → section chunks → embeddings → ChromaDB
                                                                  ↓
Question → semantic search → relevant chunks → Gemini → answer + sources
```

## Requirements

- Python 3.10 or newer
- A Google Gemini API key
- PDF documents to index

## Setup

1. Clone or extract this project, then open a terminal in its root folder.

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Gemini API key:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. Create a `documents/` directory and place the PDFs you want to search inside it:

   ```text
   documents/
   ├── employee_handbook.pdf
   ├── expense_policy.pdf
   └── product_manual.pdf
   ```

## Build the knowledge base

Run the ingestion script after adding or changing documents:

```bash
python build_vector_db.py
```

This extracts text from every PDF in `documents/`, chunks the content, generates embeddings, and writes the searchable index to `chroma_db/`.

> The current chunker is designed for documents that use numbered section headings such as `1.1` or `2.3`. Content without those headings may not be indexed as expected.

## Run the app

Once the knowledge base has been built, start Streamlit:

```bash
streamlit run app.py
```

Open the local URL displayed by Streamlit, enter a question, and select **Ask Question**. The app returns an answer followed by the source document and section names used during retrieval.

## Project structure

```text
.
├── app.py                 # Streamlit user interface
├── build_vector_db.py     # PDF ingestion and indexing entry point
├── documents/             # Add searchable PDFs here (create if absent)
├── chroma_db/             # Generated local vector database
├── requirements.txt       # Python dependencies