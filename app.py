import os
from collections.abc import Iterable
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🏢",
    layout="wide",
)


def add_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp { background: #f7f9fc; color: #172033; }
            .block-container { max-width: 1280px; padding-top: 2.5rem; padding-bottom: 3rem; }
            .hero { margin-bottom: 2rem; }
            .hero h1 { color: #14213d; font-size: 2.2rem; margin-bottom: .35rem; }
            .hero p { color: #5d6b82; font-size: 1.05rem; margin: 0; max-width: 760px; }
            .section-label { color: #344054; font-size: .84rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }
            .source-card {
                background: #ffffff; border: 1px solid #e4e9f1; border-radius: 10px;
                box-shadow: 0 1px 2px rgba(16, 24, 40, .04);
            }
            .source-card { padding: .85rem 1rem; margin-bottom: .6rem; }
            .source-name { color: #1d4ed8; font-weight: 650; margin-bottom: .2rem; }
            .source-section { color: #667085; font-size: .9rem; }
            [data-testid="stTextArea"] textarea {
                background-color: #eef2f6 !important;
                color: #111827 !important;
                caret-color: #111827 !important;
                -webkit-text-fill-color: #111827 !important;
            }
            [data-testid="stTextArea"] textarea::placeholder {
                color: #667085 !important;
                opacity: 1 !important;
                -webkit-text-fill-color: #667085 !important;
            }
            [data-testid="stTextArea"] textarea:focus {
                border-color: #1d4ed8 !important;
                box-shadow: 0 0 0 1px #1d4ed8 !important;
            }
            div.stButton > button { border-radius: 7px; font-weight: 600; }
            div.stButton > button[kind="primary"] { background: #1d4ed8; border-color: #1d4ed8; }
            div.stButton > button[kind="primary"]:hover { background: #1e40af; border-color: #1e40af; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def unpack_results(results: dict) -> tuple[list[str], list[dict]]:
    """Flatten Chroma's single-query response while keeping chunks and metadata aligned."""
    documents = (results.get("documents") or [[]])[0] or []
    metadatas = (results.get("metadatas") or [[]])[0] or []
    return list(documents), [metadata or {} for metadata in metadatas]


def render_sources(metadatas: Iterable[dict]) -> None:
    seen = set()
    unique_sources = []
    for metadata in metadatas:
        source = metadata.get("source", "Unknown document")
        section = metadata.get("section_title") or "Section unavailable"
        key = (source, section)
        if key not in seen:
            seen.add(key)
            unique_sources.append((source, section))

    if not unique_sources:
        st.caption("No source metadata was returned for this answer.")
        return

    for source, section in unique_sources:
        st.markdown(
            f'<div class="source-card"><div class="source-name">{source}</div>'
            f'<div class="source-section">Section: {section}</div></div>',
            unsafe_allow_html=True,
        )


def answer_question(question: str) -> tuple[str, list[dict]]:
    """Use the existing retrieval and Gemini answer-generation functions."""
    from src.retriever import retrieve
    from src.llm import generate_answer

    results = retrieve(question)
    chunks, metadatas = unpack_results(results)
    if not chunks:
        raise LookupError("No relevant knowledge-base content was found.")

    return generate_answer(question, chunks), metadatas


def main() -> None:
    add_styles()

    st.markdown(
        """
        <div class="hero">
            <h1>Enterprise Knowledge Assistant</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    question = st.text_area(
        "Ask a question",
        placeholder="Search enterprise policies, operational procedures, manuals, and product documentation using AI-powered retrieval.",
        height=130,
        key="question_input",
        label_visibility="collapsed",
    )
    ask_clicked = st.button("Ask Question", type="primary")

    if not ask_clicked:
        return

    if not question.strip():
        st.warning("Enter a question before searching the knowledge base.")
        return

    if not os.getenv("GEMINI_API_KEY"):
        st.error("Gemini is not configured. Add GEMINI_API_KEY to your .env file and restart the app.")
        return

    try:
        with st.spinner("Searching enterprise knowledge base..."):
            answer, metadatas = answer_question(question.strip())
    except LookupError as error:
        st.info(str(error))
        return
    except Exception:
        st.error("We couldn't complete that request. Please check the knowledge-base and Gemini configuration, then try again.")
        return

    st.markdown('<p class="section-label">Answer</p>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(answer)

    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Sources Used</p>', unsafe_allow_html=True)
    render_sources(metadatas)


if __name__ == "__main__":
    main()
