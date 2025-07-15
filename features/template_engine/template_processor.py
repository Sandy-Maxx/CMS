from docx import Document
import re
from features.template_engine.special_placeholder_handler import evaluate_special_placeholder

class TemplateProcessor:
    def __init__(self):
        pass

    def extract_placeholders(self, doc_path):
        document = Document(doc_path)
        all_found_placeholders = set()

        def _extract_from_text(text_content):
            # Find all placeholders in the text content
            found = re.findall(r"\{\{([a-zA-Z0-9_.]+)\}\}", text_content)
            for p in found:
                all_found_placeholders.add(p)

        # Extract from paragraphs in the main body
        for paragraph in document.paragraphs:
            _extract_from_text(paragraph.text)

        # Extract from tables in the main body
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        _extract_from_text(paragraph.text)

        # Extract from headers and footers
        for section in document.sections:
            # Headers
            header = section.header
            for paragraph in header.paragraphs:
                _extract_from_text(paragraph.text)
            for table in header.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            _extract_from_text(paragraph.text)

            # Footers
            footer = section.footer
            for paragraph in footer.paragraphs:
                _extract_from_text(paragraph.text)
            for table in footer.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            _extract_from_text(paragraph.text)

        # Filter for base placeholders only
        base_placeholders_for_gui = set()
        for p_name in all_found_placeholders:
            # A placeholder is considered 'base' if it does not match a derived pattern
            # Derived patterns are like COST_0.2, COST_1.18_IN_WORDS, etc.
            # We assume any placeholder starting with COST, COSTAMC, COSTRP, COSTCON, COSTCAMC
            # followed by an underscore and a number/IN_WORDS/0/00 is derived.
            is_derived = False
            if p_name.startswith(("COST", "COSTAMC", "COSTRP", "COSTCON", "COSTCAMC")):
                if re.search(r"_([0-9.]+)$|_IN_WORDS$|_0$|_00$", p_name):
                    is_derived = True
            
            # Date placeholders like CONTRACT_DATE, START_DATE, END_DATE are considered base
            # and should be displayed in the GUI.
            # The prompt states: "Input fields that contain “DATE” in their name use a date picker widget in the GUI."
            # This implies they are base placeholders for input.
            # We need to ensure that DATE placeholders are always treated as base, even if they have underscores
            if p_name.startswith("DATE"):
                is_derived = False # Dates are always base for GUI input

            if not is_derived:
                base_placeholders_for_gui.add(p_name)
        
        return base_placeholders_for_gui

    def replace_placeholders(self, doc_path, data, output_path):
        document = Document(doc_path)

        # Process paragraphs in the main body
        for paragraph in document.paragraphs:
            self._replace_in_paragraph(paragraph, data)

        # Process tables in the main body
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._replace_in_paragraph(paragraph, data)

        # Process headers and footers
        for section in document.sections:
            # Headers
            header = section.header
            for paragraph in header.paragraphs:
                self._replace_in_paragraph(paragraph, data)
            for table in header.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            self._replace_in_paragraph(paragraph, data)

            # Footers
            footer = section.footer
            for paragraph in footer.paragraphs:
                self._replace_in_paragraph(paragraph, data)
            for table in footer.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            self._replace_in_paragraph(paragraph, data)

        document.save(output_path)
        return True

    def _replace_in_paragraph(self, paragraph, data):
        # Combine all runs into a single string for easier regex matching
        full_text = "".join([run.text for run in paragraph.runs])
        
        # Find all placeholders
        # Regex to match {{PLACEHOLDER_NAME}}
        # This regex is more robust for variations like {{COST_0.2}}, {{DATE_START}}
        matches = list(re.finditer(r"\{\{([a-zA-Z0-9_.]+)\}\}", full_text))

        if not matches:
            return

        # Create a new list of runs to rebuild the paragraph
        new_runs_data = []
        last_idx = 0

        for match in matches:
            placeholder_full = match.group(0)  # e.g., {{COST_0.2}}
            placeholder_name = match.group(1)  # e.g., COST_0.2

            # Add text before the current placeholder
            if match.start() > last_idx:
                new_runs_data.append({'text': full_text[last_idx:match.start()], 'style': None})

            # Use the new evaluate_special_placeholder function
            replacement_value = evaluate_special_placeholder(placeholder_name, data)
            new_runs_data.append({'text': str(replacement_value), 'style': None}) # Store as string

            last_idx = match.end()

        # Add any remaining text after the last placeholder
        if last_idx < len(full_text):
            new_runs_data.append({'text': full_text[last_idx:], 'style': None})

        # Clear existing runs and add new ones
        for i in reversed(range(len(paragraph.runs))):
            p = paragraph.runs[i]
            p.element.getparent().remove(p.element)

        for run_data in new_runs_data:
            new_run = paragraph.add_run(run_data['text'])
            if run_data['style']:
                new_run.style = run_data['style']
