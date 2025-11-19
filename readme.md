# PDF to Structured Information Excel Extractor

**Live:**

## Overview

This project provides a user-friendly, AI-powered tool for converting unstructured PDF documents into fully structured Excel files. Using modern LLMs and a simple upload interface you can extract **all text**, detect key:value pairs with context, preserve original language, and export the output to `.xlsx`.  
It is ideal for applications such as document ingestion, data extraction, automation of manual document processing, and internal tools for analytic teams.

## How to Use the Application

**1. Upload your PDF file**

Click on the “Upload PDF” button and select the document from which you want to extract information.

**2. Click “Process Document”**

The app will extract all text from the PDF, detect key–value pairs (if possible), and structure everything properly.

**3. View the Generated Excel Output**

Once processing is finished, the app will display a preview and automatically generate an Excel file named generated-output.xlsx.

**4. Download the Excel File**

Scroll down to the Download section and click the “Download generated-output.xlsx” button to save the structured file to your system

---

## Features

- Upload any PDF (plain text or scanned).
- Robust extraction using `pdfplumber` and fallback OCR using `pytesseract`.
- Smart Key:Value detection and contextual comment derivation via LLM.
- Maintains **100% of document content** (no summarization or omission).
- Preserves original language and multi-line/complex textual structures.
- Export results to Excel (`Output.xlsx`) immediately downloadable via UI.
- Click-and-run: minimal configuration, works locally or deployed.

---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-pdf-structuring.git
   cd ai-pdf-structuring
   ```
