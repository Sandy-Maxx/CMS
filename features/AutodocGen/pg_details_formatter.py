from utils.helpers import format_currency_inr
from database.db_manager import get_unique_firm_names_by_work_id

class PGDetailsFormatter:
    def format_pg_details(self, pg_details, work_id):
        if not pg_details:
            return "No Performance Guarantee details found for this work."

        all_firms = get_unique_firm_names_by_work_id(work_id)
        submitted_firms = set(doc[2] for doc in pg_details)

        details_list = []
        for i, firm_name in enumerate(all_firms, 1):
            firm_docs = [doc for doc in pg_details if doc[2] == firm_name]

            if firm_docs:
                for doc in firm_docs:
                    pg_submitted = doc[11]
                    if pg_submitted == 1:
                        pg_no = doc[3] if doc[3] is not None else '---'
                        submission_date = doc[10] if doc[10] is not None else '----'
                        pg_amount = doc[4] if doc[4] is not None else '--------'
                        bank_name = doc[5] if doc[5] is not None else 'bank name'
                        bank_address = doc[6] if doc[6] is not None else 'address'
                        
                        formatted_pg_amount = format_currency_inr(pg_amount) if pg_amount != '--------' else '--------'

                        details_list.append(
                            f"{i}. {firm_name}, submitted PG No. {pg_no}, Dated {submission_date} amount Rs. {formatted_pg_amount}, bank: {bank_name}, {bank_address}."
                        )
                    else:
                        details_list.append(f"{i}. {firm_name} did not submit the PG.")
            else:
                details_list.append(f"{i}. {firm_name} did not submit the PG.")

        return "\n".join(details_list)
