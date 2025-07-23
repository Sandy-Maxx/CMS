class PGDetailsFormatter:
    def __init__(self):
        pass

    def format_pg_details(self, pg_details_list):
        if not pg_details_list:
            return "No PG details available."

        formatted_output = "PG Details for Firms:\n\n"
        for doc in pg_details_list:
            firm_name = doc[2] # firm_name is at index 2
            pg_no = doc[3] # pg_no is at index 3
            pg_amount = doc[4] # pg_amount is at index 4
            bank_name = doc[5] # bank_name is at index 5

            formatted_output += f"Firm: {firm_name}\n"
            formatted_output += f"  PG No.: {pg_no if pg_no else 'N/A'}\n"
            formatted_output += f"  PG Amount: {pg_amount if pg_amount else 'N/A'}\n"
            formatted_output += f"  Bank: {bank_name if bank_name else 'N/A'}\n"
            formatted_output += "\n"

        return formatted_output
