from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError
import os
import fitz  # PyMuPDF

class PdfManager:
    def __init__(self):
        pass

    def merge_pdfs(self, input_paths, output_path):
        """
        Merges multiple PDF files into a single PDF file.
        :param input_paths: A list of paths to the input PDF files.
        :param output_path: The path where the merged PDF will be saved.
        :return: True if successful, False otherwise.
        """
        pdf_writer = PdfWriter()
        for path in input_paths:
            try:
                pdf_reader = PdfReader(path)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            except PdfReadError:
                print(f"Error reading PDF file: {path}. Skipping.")
                return False
            except FileNotFoundError:
                print(f"File not found: {path}. Skipping.")
                return False
        
        try:
            with open(output_path, 'wb') as out_file:
                pdf_writer.write(out_file)
            return True
        except Exception as e:
            print(f"Error saving merged PDF: {e}")
            return False

    def extract_pages(self, input_path, output_path, pages_to_extract):
        """
        Extracts specified pages from a PDF file and saves them as a new PDF.
        :param input_path: Path to the input PDF file.
        :param output_path: The path where the extracted PDF will be saved.
        :param pages_to_extract: A list of 0-indexed page numbers to extract.
        :return: True if successful, False otherwise.
        """
        try:
            pdf_reader = PdfReader(input_path)
            pdf_writer = PdfWriter()

            for page_num in pages_to_extract:
                if 0 <= page_num < len(pdf_reader.pages):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                else:
                    print(f"Warning: Page {page_num + 1} is out of bounds. Skipping.")
            
            with open(output_path, 'wb') as out_file:
                pdf_writer.write(out_file)
            return True
        except FileNotFoundError:
            print(f"File not found: {input_path}")
            return False
        except PdfReadError:
            print(f"Error reading PDF file: {input_path}")
            return False
        except Exception as e:
            print(f"Error extracting pages: {e}")
            return False

    def get_pdf_page_count(self, pdf_path):
        """
        Returns the total number of pages in a PDF file.
        :param pdf_path: Path to the PDF file.
        :return: The number of pages, or -1 if an error occurs.
        """
        try:
            pdf_reader = PdfReader(pdf_path)
            return len(pdf_reader.pages)
        except FileNotFoundError:
            print(f"File not found: {pdf_path}")
            return -1
        except PdfReadError:
            print(f"Error reading PDF file: {pdf_path}")
            return -1
        except Exception as e:
            print(f"Error getting page count: {e}")
            return -1

    def rotate_page(self, input_path, output_path, page_number, rotation_angle):
        """
        Rotates a specific page in a PDF file and saves it as a new PDF.
        :param input_path: Path to the input PDF file.
        :param output_path: The path where the modified PDF will be saved.
        :param page_number: The 0-indexed page number to rotate.
        :param rotation_angle: The angle of rotation (e.g., 90, 180, 270).
        :return: True if successful, False otherwise.
        """
        try:
            pdf_reader = PdfReader(input_path)
            pdf_writer = PdfWriter()

            for i, page in enumerate(pdf_reader.pages):
                if i == page_number:
                    page.rotate(rotation_angle)
                pdf_writer.add_page(page)
            
            with open(output_path, 'wb') as out_file:
                pdf_writer.write(out_file)
            return True
        except FileNotFoundError:
            print(f"File not found: {input_path}")
            return False
        except PdfReadError:
            print(f"Error reading PDF file: {input_path}")
            return False
        except Exception as e:
            print(f"Error rotating page: {e}")
            return False

    def delete_page(self, input_path, output_path, page_number):
        """
        Deletes a specific page from a PDF file and saves it as a new PDF.
        :param input_path: Path to the input PDF file.
        :param output_path: The path where the modified PDF will be saved.
        :param page_number: The 0-indexed page number to delete.
        :return: True if successful, False otherwise.
        """
        try:
            pdf_reader = PdfReader(input_path)
            pdf_writer = PdfWriter()

            for i, page in enumerate(pdf_reader.pages):
                if i != page_number:
                    pdf_writer.add_page(page)
            
            with open(output_path, 'wb') as out_file:
                pdf_writer.write(out_file)
            return True
        except FileNotFoundError:
            print(f"File not found: {input_path}")
            return False
        except PdfReadError:
            print(f"Error reading PDF file: {input_path}")
            return False
        except Exception as e:
            print(f"Error deleting page: {e}")
            return False

    def compress_pdf(self, input_path, output_path, compression_level):
        """
        Compresses a PDF using PyMuPDF, which can offer better compression.
        :param input_path: Path to the input PDF file.
        :param output_path: The path where the compressed PDF will be saved.
        :param compression_level: An integer from 0 to 10, where 0 is no compression and 10 is maximum compression.
        :return: True if successful, False otherwise.
        """
        try:
            doc = fitz.open(input_path)
            # Map compression_level (0-10) to garbage parameter (0-4)
            # Higher compression_level means more aggressive garbage collection.
            garbage_level = min(4, compression_level) # Map 0-10 to 0-4, clamping at 4

            doc.save(output_path, garbage=garbage_level, deflate=True, clean=True)
            doc.close()
            return True
        except FileNotFoundError:
            print(f"File not found: {input_path}")
            return False
        except Exception as e:
            print(f"Error compressing PDF: {e}")
            return False
