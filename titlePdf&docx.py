import os
import tempfile
from PyPDF2 import PdfWriter, PdfReader  # Add PdfReader import here
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document
import pdfplumber


def extract_title_from_pdf(pdf_path):
    title = ""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        first_font_size = None
        for obj in first_page.chars:
            if not first_font_size:
                first_font_size = obj['size']
            if obj['size'] == first_font_size:
                title += obj['text']
            else:
                break
    return title.strip()

def convert_docx_to_pdf(docx_path, pdf_path):
    doc = Document(docx_path)
    output = PdfWriter()
    for para in doc.paragraphs:
        bio = BytesIO()
        c = canvas.Canvas(bio, pagesize=letter)
        c.drawString(100, 750, para.text)
        c.save()
        bio.seek(0)
        input_pdf = PdfReader(bio)
        for page in input_pdf.pages:
            output.add_page(page)
    with open(pdf_path, "wb") as f:
        output.write(f)

def extract_title_from_docx(docx_path):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf_file:
        convert_docx_to_pdf(docx_path, tmp_pdf_file.name)
        return extract_title_from_pdf(tmp_pdf_file.name)

def extract_title(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.pdf':
        return extract_title_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_title_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

def main():
    file_path = 'example6.docx'  # Path to your file
    title = extract_title(file_path)
    print("Title:", title)

if __name__ == "__main__":
    main()
