from docx import Document
import re
from datetime import datetime
from features.AutodocGen.constants import USER_PLACEHOLDER_PATTERN, WORK_DATA_PLACEHOLDER_PATTERN, FIRM_PLACEHOLDER_PATTERN, ALL_FIRMS_PG_DETAILS_PATTERN
from features.template_engine.special_placeholder_handler import evaluate_special_placeholder
from features.template_engine.work_data_provider import WorkDataProvider
from features.AutodocGen.pg_details_formatter import PGDetailsFormatter
from utils.helpers import format_currency_inr

class DocumentGenerator:
    def __init__(self, data_fetcher):
        self.data_fetcher = data_fetcher
        self.pg_formatter = PGDetailsFormatter()

    def generate(self, template_path, data, output_path, is_firm_specific=False):
        document = Document(template_path)
        work_id = data.get('work_id')
        work_data_provider = WorkDataProvider(work_id)

        # Process all paragraphs in the document
        for paragraph in document.paragraphs:
            self._replace_placeholders_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)

        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._replace_placeholders_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)

        for section in document.sections:
            for paragraph in section.header.paragraphs:
                self._replace_placeholders_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)
            for table in section.header.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            self._replace_placeholders_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)
            
            for paragraph in section.footer.paragraphs:
                self._replace_placeholders_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)
            for table in section.footer.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            self._replace_placeholders_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)

        document.save(output_path)

    def _replace_placeholders_in_paragraph(self, paragraph, data, work_data_provider, is_firm_specific):
        # Regex to find [PLACEHOLDER:FORMAT] or <<PLACEHOLDER>>
        placeholder_regex = r"(\[([\w_:-]+)\])|(<<([\w_]+)>>)"
        
        replacements = {}
        full_text = "".join(run.text for run in paragraph.runs)

        # Handle the special case [ALL_FIRMS_PG_DETAILS] separately
        if "[ALL_FIRMS_PG_DETAILS]" in full_text:
            work_id = data.get('work_id')
            if work_id:
                pg_details = self.data_fetcher.fetch_all_firms_pg_details(work_id)
                replacement_value = self.pg_formatter.format_pg_details(pg_details)
            else:
                replacement_value = "N/A (Work ID not available)"
            replacements["[ALL_FIRMS_PG_DETAILS]"] = str(replacement_value)

        # Find all other placeholders
        for match in re.finditer(placeholder_regex, full_text):
            placeholder_full = match.group(0)
            
            if placeholder_full in replacements:
                continue

            key = match.group(2) or match.group(4)
            replacement_value = None

            # Handle [PLACEHOLDER]
            if match.group(1):
                # Handle Date Placeholders like [DATE:DD-MM-YYYY]
                if key.upper().startswith("DATE:"):
                    try:
                        date_format = key.split(":")[1]
                        py_format = date_format.replace("DD", "%d").replace("MM", "%m").replace("YYYY", "%Y")
                        replacement_value = datetime.now().strftime(py_format)
                    except Exception:
                        replacement_value = f"[Invalid Date Format: {key}]"
                else:
                    # Standard work data placeholder
                    replacement_value = work_data_provider.get_data(key.upper())
                    if key.upper() == "TENDER_COST":
                        replacement_value = format_currency_inr(replacement_value)

                    if replacement_value is None or "[Invalid" in str(replacement_value):
                        replacement_value = evaluate_special_placeholder(key, data)

            # Handle <<PLACEHOLDER>>
            elif match.group(3):
                if is_firm_specific:
                    current_firm_name = data.get('firm_name')
                    if current_firm_name:
                        firm_document_data = work_data_provider.get_firm_document_data(current_firm_name)
                        
                        # Use lowercase key for lookup in the dictionary
                        lookup_key = key.lower()

                        if lookup_key == 'firm_name':
                            replacement_value = current_firm_name
                        elif lookup_key == 'pg_submitted':
                            replacement_value = "submitted the PG No." if firm_document_data.get('pg_submitted') == 1 else "did not submit the PG"
                        elif lookup_key == 'indemnity_bond_submitted':
                            replacement_value = "submitted the Indemnity Bond" if firm_document_data.get('indemnity_bond_submitted') == 1 else "did not submit the Indemnity Bond"
                        elif firm_document_data and lookup_key in firm_document_data:
                            value = firm_document_data[lookup_key]
                            if lookup_key == 'pg_amount':
                                replacement_value = format_currency_inr(value)
                            else:
                                replacement_value = value
                else:
                    replacement_value = work_data_provider.get_data(key.upper())

            if replacement_value is not None and str(replacement_value).strip() != "":
                replacements[placeholder_full] = str(replacement_value)

        # Apply the replacements to the runs in the paragraph
        for placeholder, value in replacements.items():
            for run in paragraph.runs:
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, str(value))