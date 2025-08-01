from database import db_manager
from database.managers import firm_manager
from utils.helpers import format_currency_inr
from datetime import datetime
from database.managers.database_utils import get_work_columns, get_firm_documents_columns

class WorkDataProvider:
    def __init__(self, work_id):
        self.work_id = work_id
        # Fetch ALL columns using SELECT * for both tables
        self.work_details = db_manager.get_work_by_id_all_columns(work_id)
        self.firm_documents = db_manager.get_firm_documents_all_columns(work_id)
        # Fetch firm registration data (includes address)
        self.firms_data = self._get_firms_data()

    def _get_firms_data(self):
        """Get firm registration data for firms involved in this work."""
        if not self.firm_documents:
            return []
        
        # Get unique firm names from firm_documents
        firm_names = list(set(doc.get('firm_name') for doc in self.firm_documents if doc.get('firm_name')))
        
        # Fetch firm registration data for these firms
        firms_data = []
        for firm_name in firm_names:
            firm_data = firm_manager.get_firm_by_name(firm_name)
            if firm_data:
                firms_data.append(firm_data)
        
        return firms_data

    def generate_placeholders(self):
        """Generate a consolidated dictionary of all placeholders dynamically."""
        # 1. Retrieve column lists via the new helper
        work_columns = get_work_columns()
        firm_columns = get_firm_documents_columns()
        
        # 2. Generate work placeholders: [COLUMN_NAME] format
        work_placeholders = {}
        if self.work_details:
            for column in work_columns:
                work_placeholders[f'[{column.upper()}]'] = self.work_details.get(column)
        
        # 3. Generate firm placeholders: <<COLUMN_NAME>> format
        # Iterate over every firm row linked to the work
        firm_placeholders = {}
        for firm_doc in self.firm_documents:
            for column in firm_columns:
                # For multiple firms, we use the last firm's data for each placeholder
                # (This follows the original behavior but could be modified as needed)
                firm_placeholders[f'<<{column.upper()}>>'] = firm_doc.get(column)
        
        # 3.1. Add firm address placeholders from the firms table
        for firm_data in self.firms_data:
            firm_placeholders[f'<<FIRM_ADDRESS>>'] = firm_data.get('address')
            firm_placeholders[f'<<FIRM_REPRESENTATIVE>>'] = firm_data.get('representative')
        
        # 4. Generate special placeholders
        special_placeholders = {
            '[CURRENT_DATE]': datetime.now().strftime("%Y-%m-%d"),
            '[CURRENT_TIME]': datetime.now().strftime("%H:%M:%S"),
            '[FIRM_PG_DETAILS]': self._generate_firm_pg_details(),
            '[ALL_FIRMS_PG_DETAILS]': self._generate_all_firms_pg_details()
        }
        
        # 5. Create consolidated dict from dynamic creation
        consolidated_placeholders = {**work_placeholders, **firm_placeholders, **special_placeholders}
        
        # 6. Define aliases for backward compatibility or friendlier names
        # Aliases are merged AFTER dynamic creation so future columns won't break them
        aliases = {
            '[WORK_NAME]': '[NAME]',  # Map [WORK_NAME] → [NAME]
            # Add more aliases here as needed
        }
        
        # 7. Apply aliases by checking if the target placeholder exists
        for alias_key, target_key in aliases.items():
            if target_key in consolidated_placeholders:
                consolidated_placeholders[alias_key] = consolidated_placeholders[target_key]
        
        return consolidated_placeholders

    def _generate_firm_pg_details(self):
        """Generate FIRM_PG_DETAILS multi-line string from firm rows."""
        if not self.firm_documents:
            return ""
        
        details_list = []
        for i, firm_doc in enumerate(self.firm_documents):
            pg_status = "submitted the PG No." if firm_doc.get('pg_submitted') == 1 else "did not submit the PG"
            
            # Format PG Amount with Indian Rupee symbol
            pg_amount = firm_doc.get('pg_amount')
            formatted_pg_amount = format_currency_inr(pg_amount) if pg_amount is not None else 'N/A'
            
            details_list.append(
                f"{i+1}. {firm_doc.get('firm_name', 'N/A')} {pg_status} {firm_doc.get('pg_no') or 'N/A'}, "
                f"Dated: {firm_doc.get('submission_date') or 'N/A'}, Amount: Rs. {formatted_pg_amount}, "
                f"Bank details: {firm_doc.get('bank_name') or 'N/A'}, "
                f"Address: {firm_doc.get('bank_address') or 'N/A'}."
            )
        
        return "\n".join(details_list)
    
    def _generate_all_firms_pg_details(self):
        """Generate ALL_FIRMS_PG_DETAILS multi-line string from all firm rows."""
        # For now, this is the same as _generate_firm_pg_details
        # But it could be extended to include additional details per firm
        return self._generate_firm_pg_details()
    
    def get_firm_document_data(self, firm_name):
        """Get firm document data for a specific firm name."""
        for firm_doc in self.firm_documents:
            if firm_doc.get('firm_name') == firm_name:
                return firm_doc
        return None

    def get_firm_names_list(self):
        """Get comma-separated list of firm names for this work."""
        firm_names = [doc.get('firm_name') for doc in self.firm_documents if doc.get('firm_name')]
        return ', '.join(firm_names)

    def get_firm_pg_details_block(self):
        """Legacy method - now delegates to the new implementation."""
        return self._generate_firm_pg_details()
    
    def get_available_placeholders(self):
        """Get a dictionary of all available placeholders with their descriptions."""
        # Get column lists
        work_columns = get_work_columns()
        firm_columns = get_firm_documents_columns()
        
        placeholders = {}
        
        # Work placeholders with descriptions
        work_descriptions = {
            'id': 'Work unique identifier',
            'name': 'Work name/title',
            'description': 'Work description',
            'justification': 'Work justification text',
            'section': 'Work section',
            'file_no': 'File number',
            'estimate_no': 'Estimate number',
            'admin_approval_office_note_no': 'Admin approval office note number',
            'admin_approval_date': 'Administrative approval date',
            'concurrence_letter_no': 'Concurrence letter number',
            'concurrence_letter_dated': 'Concurrence letter date',
            'dr_dfm_eoffice_note_no': 'DR/DFM eOffice note number',
            'computer_no': 'Computer number',
            'work_type': 'Complete work type (category + subcategory)',
            'work_type_category': 'Work category (DRM Power/Sr.DEE Power/HQ Power)',
            'work_type_subcategory': 'Work subcategory (M&P/RSP/SERVICE)',
            'tender_cost': 'Tender cost amount',
            'tender_opening_date': 'Date of tender opening',
            'loa_no': 'Letter of Acceptance number',
            'loa_date': 'LOA issue date',
            'work_commence_date': 'Work commencement date'
        }
        
        # Add work placeholders
        for column in work_columns:
            placeholder_key = f'[{column.upper()}]'
            description = work_descriptions.get(column.lower(), f'Work {column.replace("_", " ").title()}')
            placeholders[placeholder_key] = description
        
        # Firm placeholders with descriptions
        firm_descriptions = {
            'firm_name': 'Name of the firm',
            'firm_address': 'Address of the firm',
            'pg_no': 'Performance Guarantee number',
            'pg_amount': 'Performance Guarantee amount',
            'bank_name': 'Bank name for PG',
            'bank_address': 'Bank address for PG',
            'submission_date': 'Date of document submission',
            'pg_submitted': 'Whether PG was submitted',
            'indemnity_bond_submitted': 'Whether Indemnity Bond was submitted',
            'pg_vetted_on': 'Date PG was vetted',
            'ib_vetted_on': 'Date Indemnity Bond was vetted',
            'pg_type': 'Type of Performance Guarantee',
            'indemnity_bond_details': 'Details of Indemnity Bond',
            'other_docs_details': 'Details of other documents'
        }
        
        # Add firm placeholders
        for column in firm_columns:
            placeholder_key = f'<<{column.upper()}>>'
            description = firm_descriptions.get(column.lower(), f'Firm {column.replace("_", " ").title()}')
            placeholders[placeholder_key] = description
        
        # Add firm address and representative placeholders from firms table
        placeholders['<<FIRM_ADDRESS>>'] = 'Address of the firm (from firm registration)'
        placeholders['<<FIRM_REPRESENTATIVE>>'] = 'Representative of the firm (from firm registration)'
        
        # Add special placeholders
        special_placeholders = {
            '[CURRENT_DATE]': 'Today\'s date (auto-generated)',
            '[CURRENT_TIME]': 'Current time (auto-generated)',
            '[FIRM_PG_DETAILS]': 'Formatted list of all firms\' PG details',
            '[ALL_FIRMS_PG_DETAILS]': 'Complete PG details for all firms',
            '[ENQUIRY_TABLE]': 'Creates a formatted enquiry table with schedule items, quantities, unit rates, and totals'
        }
        
        placeholders.update(special_placeholders)
        
        # Add aliases
        aliases = {
            '[WORK_NAME]': 'Alias for [NAME] - Work name/title'
        }
        
        placeholders.update(aliases)
        
        return placeholders
    
    @staticmethod
    def get_available_placeholders_static():
        """Static method to get available placeholders without needing a work_id."""
        # Get column lists
        work_columns = get_work_columns()
        firm_columns = get_firm_documents_columns()
        
        placeholders = {}
        
        # Work placeholders with descriptions
        work_descriptions = {
            'id': 'Work unique identifier',
            'name': 'Work name/title', 
            'description': 'Work description',
            'justification': 'Work justification text',
            'section': 'Work section',
            'file_no': 'File number',
            'estimate_no': 'Estimate number',
            'admin_approval_office_note_no': 'Admin approval office note number',
            'admin_approval_date': 'Administrative approval date',
            'concurrence_letter_no': 'Concurrence letter number',
            'concurrence_letter_dated': 'Concurrence letter date',
            'dr_dfm_eoffice_note_no': 'DR/DFM eOffice note number',
            'computer_no': 'Computer number',
            'work_type': 'Complete work type (category + subcategory)',
            'work_type_category': 'Work category (DRM Power/Sr.DEE Power/HQ Power)',
            'work_type_subcategory': 'Work subcategory (M&P/RSP/SERVICE)',
            'tender_cost': 'Tender cost amount',
            'tender_opening_date': 'Date of tender opening',
            'loa_no': 'Letter of Acceptance number',
            'loa_date': 'LOA issue date',
            'work_commence_date': 'Work commencement date'
        }
        
        # Add work placeholders
        for column in work_columns:
            placeholder_key = f'[{column.upper()}]'
            description = work_descriptions.get(column.lower(), f'Work {column.replace("_", " ").title()}')
            placeholders[placeholder_key] = description
        
        # Firm placeholders with descriptions
        firm_descriptions = {
            'firm_name': 'Name of the firm',
            'firm_address': 'Address of the firm',
            'pg_no': 'Performance Guarantee number',
            'pg_amount': 'Performance Guarantee amount',
            'bank_name': 'Bank name for PG',
            'bank_address': 'Bank address for PG',
            'submission_date': 'Date of document submission',
            'pg_submitted': 'Whether PG was submitted',
            'indemnity_bond_submitted': 'Whether Indemnity Bond was submitted',
            'pg_vetted_on': 'Date PG was vetted',
            'ib_vetted_on': 'Date Indemnity Bond was vetted',
            'pg_type': 'Type of Performance Guarantee',
            'indemnity_bond_details': 'Details of Indemnity Bond',
            'other_docs_details': 'Details of other documents'
        }
        
        # Add firm placeholders
        for column in firm_columns:
            placeholder_key = f'<<{column.upper()}>>'  
            description = firm_descriptions.get(column.lower(), f'Firm {column.replace("_", " ").title()}')
            placeholders[placeholder_key] = description
        
        # Add firm address and representative placeholders from firms table
        placeholders['<<FIRM_ADDRESS>>'] = 'Address of the firm (from firm registration)'
        placeholders['<<FIRM_REPRESENTATIVE>>'] = 'Representative of the firm (from firm registration)'
        
        # Add special placeholders
        special_placeholders = {
            '[CURRENT_DATE]': 'Today\'s date (auto-generated)',
            '[CURRENT_TIME]': 'Current time (auto-generated)',
            '[FIRM_PG_DETAILS]': 'Formatted list of all firms\' PG details',
            '[ALL_FIRMS_PG_DETAILS]': 'Complete PG details for all firms',
            '[ENQUIRY_TABLE]': 'Creates a formatted enquiry table with schedule items, quantities, unit rates, and totals'
        }
        
        placeholders.update(special_placeholders)
        
        # Add aliases
        aliases = {
            '[WORK_NAME]': 'Alias for [NAME] - Work name/title'
        }
        
        placeholders.update(aliases)
        
        return placeholders
    
    def get_data(self, key):
        """Get data for a specific placeholder key with alias support."""
        # Define aliases for backward compatibility or friendlier names
        # Aliases are merged AFTER dynamic creation so future columns won't break them
        aliases = {
            'WORK_NAME': 'NAME',  # Map [WORK_NAME] → [NAME]
            # Add more aliases here as needed
        }
        
        # Check if the key is an alias, if so use the actual column name
        actual_key = aliases.get(key, key)
        
        # Try to get data from work_details first
        if self.work_details and actual_key.lower() in self.work_details:
            return self.work_details[actual_key.lower()]
        
        # Handle special cases
        if key == 'CURRENT_DATE':
            return datetime.now().strftime("%Y-%m-%d")
        elif key == 'CURRENT_TIME':
            return datetime.now().strftime("%H:%M:%S")
        elif key == 'FIRM_PG_DETAILS':
            return self._generate_firm_pg_details()
        elif key == 'ALL_FIRMS_PG_DETAILS':
            return self._generate_all_firms_pg_details()
        
        # Return None if key not found (will be handled by caller)
        return None
