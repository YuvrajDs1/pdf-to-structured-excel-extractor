import streamlit as st
import pandas as pd
import re
import io
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import fitz
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.environ["GROQ_API_KEY"]

def extract_pdf_text(file):
    """Safe text extraction with fallback modes."""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""

    for page in pdf:
        try:
            page_text = page.get_text("text")
        except:
            page_text = page.get_text()
        
        if not isinstance(page_text, str):
            page_text = str(page_text)

        text += page_text + "\n"

    return text

def extract_kv_pairs(text):
    """
    Extract approximate key:value pairs using regex.
    LLM will refine later.
    """
    pattern = r"([A-Za-z0-9 \-/]+)\s*[:\-]\s*([^\n]+)"
    matches = re.findall(pattern, text)

    pairs = []
    for key, value in matches:
        pairs.append({"key": key.strip(), "value": value.strip()})

    return pairs

def refine_with_llm(text, raw_pairs):
    llm = ChatGroq(model="llama-3.1-8b-instant")

    prompt = ChatPromptTemplate.from_template("""
You are an AI specialized in reading unstructured documents and producing structured key:value relationships.

INPUT DOCUMENT:
---------------------
{text}
---------------------

EXTRACTED RAW PAIRS:
{raw_pairs}

TASK:
- Clean keys (but do NOT paraphrase values).
- Ensure every piece of information from the document is captured.
- Add missing items that regex could not extract.
- Keep exact original language in values and comments.
- Output ONLY valid JSON in the following format:

[
  {{
    "key": "KEY HERE",
    "value": "VALUE HERE",
    "comments": "COMMENTS HERE"
  }}
]

Make sure:
- Use double quotes for all JSON fields.
- Do NOT include backticks, markdown, or explanations.
""")

    result = (prompt | llm | StrOutputParser()).invoke({
        "text": text,
        "raw_pairs": raw_pairs
    })

    try:
        return eval(result)
    except:
        return []

def convert_to_excel(rows):
    df = pd.DataFrame(rows)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    return output.getvalue()


st.set_page_config(page_title="AI-Powered Document Structuring", layout="wide")
st.title("📄 AI-Powered Document Structuring & Extraction Tool")

uploaded = st.file_uploader("Upload Data Input.pdf", type=["pdf"])

if uploaded:
    st.success("PDF uploaded successfully!")

    with st.spinner("Extracting text..."):
        text = extract_pdf_text(uploaded)

    st.subheader("🔍 Extracted Text Preview")
    st.text_area("", text[:4000], height=300)

    if st.button("Process Document"):
        with st.spinner("Extracting key:value pairs..."):
            raw_pairs = extract_kv_pairs(text)

        st.write("### Raw Pairs Extracted (Regex)")
        st.json(raw_pairs[:10])

        with st.spinner("Refining using LLM..."):
            final_rows = refine_with_llm(text, raw_pairs)

        st.success("Processing complete!")

        st.write("### Final Structured Output")
        st.write("Please Re-run the Page Case of Empty Output")

        excel_bytes = convert_to_excel(final_rows)
        st.dataframe(pd.DataFrame(final_rows))
        st.download_button(
            label="📥 Download Generated Output.xlsx",
            data=excel_bytes,
            file_name="Generated-Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
