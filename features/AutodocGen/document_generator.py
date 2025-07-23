from docx import Document
import re
from features.AutodocGen.constants import USER_PLACEHOLDER_PATTERN, WORK_DATA_PLACEHOLDER_PATTERN, FIRM_PLACEHOLDER_PATTERN
from features.template_engine.special_placeholder_handler import evaluate_special_placeholder
from features.template_engine.work_data_provider import WorkDataProvider
from features.AutodocGen.pg_details_formatter import PGDetailsFormatter

class DocumentGenerator:
    def __init__(self, data_fetcher):
        self.data_fetcher = data_fetcher
        self.pg_formatter = PGDetailsFormatter()

    def generate(self, template_path, data, output_path, is_firm_specific=False):
        document = Document(template_path)
        work_id = data.get('work_id') # Assuming work_id is passed in data
        work_data_provider = WorkDataProvider(work_id)

        # Process paragraphs in the main body
        for paragraph in document.paragraphs:
            self._replace_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)

        # Process tables in the main body
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._replace_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)

        # Process headers and footers
        for section in document.sections:
            # Headers
            header = section.header
            for paragraph in header.paragraphs:
                self._replace_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)
            for table in header.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            self._replace_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)

            # Footers
            footer = section.footer
            for paragraph in footer.paragraphs:
                self._replace_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)
            for table in footer.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            self._replace_in_paragraph(paragraph, data, work_data_provider, is_firm_specific)

        document.save(output_path)

    def _replace_in_paragraph(self, paragraph, data, work_data_provider, is_firm_specific, firm_name=None):
        full_text = "".join([run.text for run in paragraph.runs])
        
        # Combined regex for all placeholder types
        matches = list(re.finditer(r"(\{\{([a-zA-Z0-9_.]+)\}\}\]|\[([a-zA-Z0-9_]+)\]|<<([a-zA-Z0-9_]+)>>|\[ALL_FIRMS_PG_DETAILS\])", full_text))

        if not matches:
            return

        new_runs_data = []
        last_idx = 0

        for match in matches:
            placeholder_full = match.group(0)
            user_input_ph = match.group(2)
            work_data_ph = match.group(3)
            firm_ph = match.group(4)

            if match.start() > last_idx:
                new_runs_data.append({'text': full_text[last_idx:match.start()], 'style': None})

            replacement_value = None

            if placeholder_full == "[ALL_FIRMS_PG_DETAILS]":
                work_id = data.get('work_id')
                if work_id:
                    pg_details = self.data_fetcher.fetch_all_firms_pg_details(work_id)
                    replacement_value = self.pg_formatter.format_pg_details(pg_details)
                else:
                    replacement_value = "N/A (Work ID not available)"
            elif user_input_ph:
                replacement_value = evaluate_special_placeholder(user_input_ph, data)
            elif work_data_ph:
                replacement_value = work_data_provider.get_data(work_data_ph)
            elif firm_ph and is_firm_specific:
                # Assuming firm_name is available in data if is_firm_specific is True
                current_firm_name = data.get('firm_name') 
                if current_firm_name:
                    firm_document_data = work_data_provider.get_firm_document_data(current_firm_name)
                    if firm_ph == 'firm_name':
                        replacement_value = current_firm_name
                    elif firm_ph == 'pg_submitted':
                        replacement_value = "submitted the PG No." if firm_document_data.get('pg_submitted') == 1 else "did not submit the PG"
                    elif firm_ph == 'indemnity_bond_submitted':
                        replacement_value = "submitted the Indemnity Bond" if firm_document_data.get('indemnity_bond_submitted') == 1 else "did not submit the Indemnity Bond"
                    elif firm_document_data and firm_ph in firm_document_data:
                        replacement_value = firm_document_data[firm_ph]

            if replacement_value is None or str(replacement_value).strip() == "":
                new_runs_data.append({'text': placeholder_full, 'style': None})
            else:
                new_runs_data.append({'text': str(replacement_value), 'style': None})

            last_idx = match.end()

        if last_idx < len(full_text):
            new_runs_data.append({'text': full_text[last_idx:], 'style': None})

        for i in reversed(range(len(paragraph.runs))):
            p = paragraph.runs[i]
            p.element.getparent().remove(p.element)

        for run_data in new_runs_data:
            new_run = paragraph.add_run(run_data['text'])
            if run_data['style']:
                new_run.style = run_data['style']
