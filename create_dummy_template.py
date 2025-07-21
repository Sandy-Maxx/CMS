
from docx import Document

def create_dummy_template():
    document = Document()
    document.add_paragraph('Hello, {{NAME}}! This is a test document for work [work_name].')
    document.save('test_template.docx')

if __name__ == '__main__':
    create_dummy_template()
