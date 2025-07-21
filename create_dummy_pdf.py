
from PyPDF2 import PdfWriter

def create_dummy_pdf():
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)  # US Letter size
    writer.add_blank_page(width=612, height=792)
    with open("dummy.pdf", "wb") as f:
        writer.write(f)

if __name__ == '__main__':
    create_dummy_pdf()
