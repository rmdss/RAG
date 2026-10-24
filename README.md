# PDF Question Answering using RAG — Execution Guide

## 1. Project Overview

This project was implemented following the tutorial, https://www.youtube.com/watch?v=2TJxpyO3ei4.

**Note:** Some files from the original tutorial were modified to resolve compatibility issues with newer LangChain and ChromaDB versions and to enable local execution using Ollama instead of AWS Bedrock. The modified files include `populate_database.py`, `get_embedding_function.py`, and `query_data.py`.

This project allows users to ask questions about PDF documents using Retrieval-Augmented Generation (RAG). It uses LangChain to orchestrate the workflow, ChromaDB to store and retrieve document embeddings, Ollama to run the language model locally, and `nomic-embed-text` to generate embeddings.

## 2. Prerequisites

Install the following software:

- Python 3.11
- Anaconda
- Visual Studio Code
- Ollama for Windows

Download Ollama from https://ollama.com/download/windows.

## 3. Project Structure

The project directory should contain the following files and folders:

```text
C:\Practicals\RAG\
│
├── data\                       # Source PDF documents
├── chroma\                     # Generated vector database
├── populate_database.py        # Document ingestion
├── query_data.py               # Question answering
├── get_embedding_function.py   # Embedding configuration
└── requirements.txt            # Python dependencies
```

The `chroma` folder is generated when the database is created. The `data` folder should contain the PDF files to be processed.

## 4. Create and Activate the Python Environment

Open PowerShell in VS Code and navigate to the project directory.

```powershell
cd C:\Practicals\RAG
```

Create a dedicated environment (only required once):

```powershell
conda create -n rag-tutorial python=3.11 -y
```

Activate it:

```powershell
conda activate rag-tutorial
```

Verify the Python version:

```powershell
python --version
```

Expected output: Python 3.11.x.

If the environment already exists, simply activate it instead of creating it again.

## 5. Install Python Dependencies

Upgrade pip and install the packages required by the current implementation:

```powershell
python -m pip install --upgrade pip
python -m pip install langchain-community langchain-core langchain-chroma chromadb langchain-ollama pypdf
```

Verify that the main packages are installed:

```powershell
python -m pip list
```

Note: A deprecation warning from `langchain-community` may appear. A warning alone does not prevent execution.

## 6. Configure Ollama and Download the Models

Ensure that Ollama is installed and running. Open PowerShell and verify its availability:

```powershell
ollama --version
```

Download the embedding model:

```powershell
ollama pull nomic-embed-text
```

Download the chat model:

```powershell
ollama pull mistral
```

Verify the installed models:

```powershell
ollama list
```

Both `nomic-embed-text` and `mistral` should appear in the output.

The embedding model converts text into vectors for similarity search, while Mistral generates answers from the retrieved document content.

## 7. Prepare the PDF Documents

Place one or more readable PDF files inside:

```text
C:\Practicals\RAG\data\
```

Ensure the PDFs contain extractable text. Scanned PDFs may require OCR if their text cannot be extracted directly.

## 8. Configure the Embedding Function

Open `get_embedding_function.py` and verify that it contains:

```python
from langchain_ollama import OllamaEmbeddings


def get_embedding_function():
    return OllamaEmbeddings(
        model="nomic-embed-text"
    )
```

This configures the application to generate embeddings locally using Ollama without requiring AWS credentials.

## 9. Populate the Chroma Vector Database

Run the following command from the project root:

```powershell
python populate_database.py
```

The script performs these operations:

1. Loads the PDF documents from the `data` directory.
2. Splits document text into smaller chunks.
3. Generates embeddings for the chunks.
4. Stores the embeddings and associated document content in ChromaDB.
5. Checks existing document IDs to avoid inserting duplicate chunks.

An example output is:

```text
Number of existing documents in DB: 0
Adding new documents: 40
```

The actual number of chunks depends on the documents.

Modern Chroma integrations persist data automatically. Do not call `db.persist()` if your installed version does not support that method.

If the output indicates that existing documents are already in the database, the script may have completed ingestion during an earlier run.

## 10. Execute the Question-Answering Script

Ensure that `query_data.py` uses the following imports:

```python
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
```

The script should load the existing Chroma database using the same embedding model used during ingestion, retrieve relevant document chunks, and pass the context to Mistral.

Run a query from PowerShell:

```powershell
python query_data.py "What is this document about?"
```

Replace the question with one relevant to your PDFs.

The application retrieves the five most relevant chunks, generates an answer using Mistral, and prints the answer along with source references.

## 11. Example Queries

Try questions such as:

```text
What is the main topic of the document?
```

```text
What are the key findings discussed in the document?
```

```text
Summarize the main points covered in the document.
```

For better results, ask specific questions that can be answered using the content of the PDFs.

## 12. Troubleshooting

| Problem | Recommended action |
|---|---|
| `ModuleNotFoundError` | Activate the correct Conda environment and install the missing package. |
| AWS credentials error | Verify that `get_embedding_function.py` uses `OllamaEmbeddings` rather than `BedrockEmbeddings`. |
| Ollama connection error | Ensure that Ollama is running and accessible. |
| Model not found | Run `ollama pull mistral` or `ollama pull nomic-embed-text`, as appropriate. |
| `db.persist()` error | Remove the call if the installed Chroma version persists data automatically. |
| No PDF documents found | Check that the PDF files are inside the `data` directory. |
| Irrelevant answers | Verify the extracted text, retrieved chunks, embedding model, and question. |
| Changes to PDFs are not reflected | Check the ingestion script's document-ID logic and reprocess the changed documents as necessary. |

## 13. Execution Workflow Summary

Whenever you want to use the application:

1. Open the project in VS Code.
2. Activate the Conda environment.
3. Ensure Ollama is running.
4. Add PDFs to the `data` folder if needed.
5. Run `python populate_database.py` when documents need ingestion.
6. Run `python query_data.py "Your question here"` to ask questions.

The database does not need to be rebuilt for every question. It can be reused across queries, provided that the same embedding model and database configuration are maintained.

## 14. Limitations

- Answer quality depends on the quality of PDF text extraction and document retrieval.
- The language model may produce incorrect answers even when prompted to use only retrieved context.
- Source references help locate supporting chunks but do not guarantee that an answer is correct.
- Local model performance depends on available RAM, CPU resources, and model size.

**Conclusion:** The application demonstrates an end-to-end RAG pipeline that combines PDF ingestion, vector embeddings, semantic retrieval, and local LLM-based answer generation. It provides a foundation for building more advanced document question-answering applications.
