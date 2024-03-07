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

def main():
    pdf_path = 'example5.pdf'  # Path to your PDF file
    title = extract_title_from_pdf(pdf_path)
    print("Title:", title)

if __name__ == "__main__":
    main()
