from utils.helpers import format_currency_inr

class PGDetailsFormatter:
    def format_pg_details(self, pg_details):
        if not pg_details:
            return "No Performance Guarantee details found for this work."

        details_list = []
        for i, doc_tuple in enumerate(pg_details):
            # Assuming the order of columns in the tuple from get_firm_documents:
            # id, work_id, firm_name, pg_no, pg_amount, bank_name, bank_address, 
            # firm_address, indemnity_bond_details, other_docs_details, submission_date, 
            # pg_submitted, indemnity_bond_submitted
            firm_name = doc_tuple[2] if doc_tuple[2] is not None else 'N/A'
            pg_submitted = doc_tuple[11]

            if pg_submitted == 1:
                pg_no = doc_tuple[3] if doc_tuple[3] is not None else '---'
                submission_date = doc_tuple[10] if doc_tuple[10] is not None else '----'
                pg_amount = doc_tuple[4] if doc_tuple[4] is not None else '--------'
                bank_name = doc_tuple[5] if doc_tuple[5] is not None else 'bank name'
                bank_address = doc_tuple[6] if doc_tuple[6] is not None else 'address'
                
                formatted_pg_amount = format_currency_inr(pg_amount) if pg_amount != '--------' else '--------'

                details_list.append(
                    f"{i+1}. {firm_name}, submitted PG No. {pg_no}, Dated {submission_date} amount Rs. {formatted_pg_amount}, bank: {bank_name}, {bank_address}."
                )
            else:
                details_list.append(f"{i+1}. {firm_name} did not submit the PG.")
        
        return "\n".join(details_list)