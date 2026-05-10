import os
import streamlit as st

from rag_pipeline import build_store_vector, retrieve_chunks, generate_results

# Sets the browser tab title and app layout
st.set_page_config(
    page_title="Financial Report Analyzer",
    layout="wide"
)

# Custom CSS for styling
# Many selectors use data-testid due to streamit class names changes often
st.markdown(
    """
    <style>

    .stApp {
        background-color: white;
        color: black;
    }
    
    /* Hides streamlit toolbar/header items */
    header,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        display: none;
        visibility: hidden;
    }

    .main-title {
        text-align: center;
        color: #15803d;
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        color: black;
        font-size: 18px;
        margin-top: 10px;
        margin-bottom: 35px;
    }

    /* File uploading styles */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploaderDropzone"] {
        background-color: #dcfce7 !important;
        color: #14532d !important;
    }

    [data-testid="stFileUploader"] {
        border: 2px solid #15803d !important;
        border-radius: 16px !important;
        padding: 24px !important;
    }

    [data-testid="stFileUploader"] * {
        color: #14532d !important;
    }

    /* Button styling */
    div.stButton > button,
    [data-testid="stFileUploader"] button {
        background-color: #15803d !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
    }

    div.stButton > button *,
    [data-testid="stFileUploader"] button * {
        color: white !important;
    }

    div.stButton > button:hover,
    [data-testid="stFileUploader"] button:hover {
        background-color: #166534 !important;
        color: white !important;
    }

    /* Custom boxes styling */
    .info-box,
    .result-box {
        background-color: #dcfce7;
        border: 2px solid #15803d;
        border-radius: 14px;
        color: #14532d;
        padding: 20px 24px;
        margin: 20px 0;
        font-size: 18px;
        font-weight: 600;
    }

    .result-box h3 {
        color: #14532d;
        margin-top: 0;
        margin-bottom: 12px;
    }

    .result-box p {
        color: #14532d;
        font-size: 17px;
        line-height: 1.6;
    }

    /* Question Styling */
    .stTextInput input {
        background-color: #dcfce7 !important;
        color: #14532d !important;
        border: 2px solid #15803d !important;
        border-radius: 12px !important;
        font-size: 16px !important;
    }

    .stTextInput input::placeholder {
        color: #3f7f57 !important;
    }

    [data-testid="stExpander"] {
        background-color: #dcfce7 !important;
        border: 2px solid #15803d !important;
        border-radius: 12px !important;
        margin-bottom: 14px !important;
    }

    [data-testid="stExpander"] summary {
        background-color: #dcfce7 !important;
        color: #14532d !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary * {
        color: #14532d !important;
    }

    [data-testid="stExpander"] div {
        background-color: #dcfce7 !important;
        color: #14532d !important;
    }
    
    /* Warning box */
    [data-testid="stAlert"] {
        background-color: #fef9c3 !important;
        border: 2px solid #ca8a04 !important;
        border-radius: 12px !important;
    }

    [data-testid="stAlert"] * {
        color: black !important;
        font-weight: 600 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.markdown(
    "<h1 class='main-title'>Financial Report Analyzer</h1>",
    unsafe_allow_html=True
)

# App subtitle
st.markdown(
    "<p class='subtitle'>Upload a corporate filing and ask questions using RAG.</p>",
    unsafe_allow_html=True
)

# Folder used to store uploaded PDFs temporarily
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# If no PDF has been uploaded, shows uploader
if "uploaded_pdf_path" not in st.session_state:
    upload_area = st.empty()

    with upload_area.container():
        uploaded_file = st.file_uploader(
            "Upload a financial filing PDF",
            type=["pdf"]
        )

    # Once file is uploaded, save it, then store the path in session_state
    if uploaded_file is not None:
        pdf_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state["uploaded_pdf_path"] = pdf_path
        st.session_state["current_pdf"] = uploaded_file.name

        # Removes the uploader and rerun for UI updates cleanly
        upload_area.empty()
        st.rerun()

# If a PDF already exists in session_state, show the uploaded file
else:
    st.markdown(
        f"<div class='info-box'>Uploaded file: {st.session_state['current_pdf']}</div>",
        unsafe_allow_html=True
    )

    # Allows user to reset the app and upload different file
    if st.button("Choose Different PDF"):
        del st.session_state["uploaded_pdf_path"]
        del st.session_state["current_pdf"]

        if "index_built" in st.session_state:
            del st.session_state["index_built"]

        st.rerun()

# Message shown before uploading
if "uploaded_pdf_path" not in st.session_state:
    st.markdown(
        "<div class='info-box'>Upload a PDF to begin.</div>",
        unsafe_allow_html=True
    )

# Build vector index after a PDF has been uploaded
if "uploaded_pdf_path" in st.session_state:
    # Only show build button before index is being built
    if not st.session_state.get("index_built"):
        if st.button("Build RAG Index"):
            with st.spinner("Reading PDF, chunking text, generating embeddings, and storing vectors..."):
                build_store_vector(st.session_state["uploaded_pdf_path"])

            st.session_state["index_built"] = True

            st.markdown(
                "<div class='info-box'>RAG index built successfully.</div>",
                unsafe_allow_html=True
            )

# Show question input only after index is built
if st.session_state.get("index_built"):
    st.markdown(
        f"<div class='info-box'>Current document: {st.session_state.get('current_pdf')}</div>",
        unsafe_allow_html=True
    )

    query = st.text_input(
        "Ask a question:",
        placeholder="Example: What were Walmart's total revenues in fiscal 2024?"
    )

    if st.button("Analyze"):
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            # Retrieves relevant chunks and generates answer
            with st.spinner("Retrieving relevant context and generating answer..."):
                results = retrieve_chunks(query, n_results=8)
                retrieved_docs = results["documents"][0]
                answer = generate_results(query, retrieved_docs)

            st.markdown(
                f"""
                <div class='result-box'>
                    <h3>AI Answer</h3>
                    <p>{answer}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Does not show sources when models says answer is unavailable
            if "I cannot determine" not in answer:
                st.markdown(
                    """
                    <div class='result-box'>
                        <h3>Retrieved Source Context</h3>
                        <p>Open each source below to view the supporting text.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Displays retrieved chunks
                for i, doc in enumerate(retrieved_docs, start=1):
                    with st.expander(f"Source {i}"):
                        st.markdown(
                            f"""
                            <div style='
                                color:#14532d;
                                background-color:#dcfce7;
                                white-space:pre-wrap;
                            '>
                            {doc[:2500]}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )