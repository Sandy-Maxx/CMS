import os
from features.pdf_tools.pdf_manager import PdfManager

def test_pdf_tools():
    print("--- Testing PDF Tools ---")
    pdf_manager = PdfManager()
    dummy_pdf = "dummy.pdf"

    # 1. Test PDF Merging
    print("\nStep 1: Testing PDF Merging...")
    merged_pdf = "merged.pdf"
    success = pdf_manager.merge_pdfs([dummy_pdf, dummy_pdf], merged_pdf)
    if success and os.path.exists(merged_pdf):
        print("SUCCESS: PDFs merged.")
        # Verify page count
        reader = pdf_manager.get_pdf_page_count(merged_pdf)
        if reader == 4:
            print("SUCCESS: Merged PDF has correct page count (4).")
        else:
            print(f"FAILURE: Merged PDF has incorrect page count ({reader}).")
        os.remove(merged_pdf)
    else:
        print("FAILURE: PDF merging failed.")

    # 2. Test Page Extraction
    print("\nStep 2: Testing Page Extraction...")
    extracted_pdf = "extracted.pdf"
    success = pdf_manager.extract_pages(dummy_pdf, extracted_pdf, [0]) # Extract first page
    if success and os.path.exists(extracted_pdf):
        print("SUCCESS: Page extracted.")
        # Verify page count
        reader = pdf_manager.get_pdf_page_count(extracted_pdf)
        if reader == 1:
            print("SUCCESS: Extracted PDF has correct page count (1).")
        else:
            print(f"FAILURE: Extracted PDF has incorrect page count ({reader}).")
        os.remove(extracted_pdf)
    else:
        print("FAILURE: Page extraction failed.")

    # 3. Test Page Rotation
    print("\nStep 3: Testing Page Rotation...")
    rotated_pdf = "rotated.pdf"
    success = pdf_manager.rotate_page(dummy_pdf, rotated_pdf, 0, 90) # Rotate first page by 90 degrees
    if success and os.path.exists(rotated_pdf):
        print("SUCCESS: Page rotated.")
        # We can't easily verify the rotation itself, but we can check if the file is valid
        reader = pdf_manager.get_pdf_page_count(rotated_pdf)
        if reader == 2:
            print("SUCCESS: Rotated PDF has correct page count (2).")
        else:
            print(f"FAILURE: Rotated PDF has incorrect page count ({reader}).")
        os.remove(rotated_pdf)
    else:
        print("FAILURE: Page rotation failed.")

    # 4. Test Page Deletion
    print("\nStep 4: Testing Page Deletion...")
    deleted_pdf = "deleted.pdf"
    success = pdf_manager.delete_page(dummy_pdf, deleted_pdf, 0) # Delete first page
    if success and os.path.exists(deleted_pdf):
        print("SUCCESS: Page deleted.")
        # Verify page count
        reader = pdf_manager.get_pdf_page_count(deleted_pdf)
        if reader == 1:
            print("SUCCESS: Deleted PDF has correct page count (1).")
        else:
            print(f"FAILURE: Deleted PDF has incorrect page count ({reader}).")
        os.remove(deleted_pdf)
    else:
        print("FAILURE: Page deletion failed.")

    # 5. Clean up
    print("\nStep 5: Cleaning up...")
    os.remove(dummy_pdf)
    print("SUCCESS: Dummy PDF deleted.")

if __name__ == '__main__':
    test_pdf_tools()
