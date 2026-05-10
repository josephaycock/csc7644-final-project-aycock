# RAG Financial Analyzer
## Project Overview
The Financial Report Analyzer is a RAG application developed for CSC 7644 - Applied LLM Development. The system allows 
a SEC filing such as 10-K, 10-Q, and 8-K documents and ask question about the documents. The application will retrieve
 the most relevant sections of the filing using vector similarity search and generates answers using LLM.
<br> The main problem being addressed by this project is the difficulty to search through the filings manually. This is
 time consuming due to the documents being hundreds of pages long. This application makes that process easier by 
automatically retrieving the relevant context and generating answers.

## Key Features / Capabilities
<ol>
    <li> Upload SEC filing PDFs
    <li> Automatically extracts filing texts
    <li> Split filings into overlapping chunks
    <li> Generates embeddings using OpenAI embedding API
    <li> Stores vectors locally using ChromaDB
    <li> Retrieves relevant chunks from filings
    <li> Generates answers using GPT-4o-mini
    <li> Displays retrieved sources
    <li> Web interface build with Streamlit
    <li> Metedata extraction for:
        <ol>
            <li> Company Name
            <li> Filing Type
            <li> Year
            <li> Path
        </ol>
</ol>

## Tech Stack and Architecture
### Technologies used
<ul>
    <li> Frontend - Streamlit
    <li> LLM -  GPT-4o-mini
    <li> Embedding - text-embedding-3-small
    <li> Vector Database - ChromaDB
    <li> PDF Parsing - PyPDF
    <li> Language - Python
    <li> Retrieval Method - Semantic Vector Search
    <li> CLI Parsing - argparse
</ul>

### System Architecture
This system follows a RAG workflow:
<ol>
    <li> User uploads a financial filing PDF
    <li> PDF text is extracted using PyPDF
    <li> Text is chunked into overlapping sections
    <li> Each chunk is converted into embeddings
    <li> User submits a question
    <li> The question is embedded
    <li> ChromaDB retrieves the most relevant chunks
    <li> Retrieved context is passed to GPT-4o-mini
    <li> THe model generates an answer
</ol>

## Setup Instructions
### Prerequisites
This is mainly for MacOS but with windows do not include "3"!
<ul>
    <li> Python 3.10+
    <li> OpenAI API key
    <li> pip package manager
</ul>

### Install Dependencies
Create and activate a virtual environment
<br>`python3 -m venv venv`
<br>`source venv/bin/activate`
<br> Install required packages
<br> `pip install -r requirements.txt`

### Configure Environment Variables
Create a .env file:
<br> `OPENAI_API_KEY=your_api_key_here`

### Running the Application
`streamlit run app.py`

## File Descriptions
<ul>
    <li> app.py - Streamlit Frontend
    <li> main.py - CLI (not for user use this was for testing)
    <li> rag_pipeline.py - RAG Workflow
    <li> pdf_loader.py - PDF Text Extraction
    <li> text_chunker.py - Chunking logic
    <li> metadata_extractor.py - Extract Filing Metadata
    <li> chroma_db/ - Local Vector Database
    <li> data/raw/ - Sample SEC Filings
</ul>