
import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from openpyxl import Workbook

# Add the project root to Python path for imports
sys.path.insert(0, os.path.abspath('../..'))

from writer import write_work_name_row, write_summary_section
from constants import COLUMN_HEADERS

class TestExcelWriter(unittest.TestCase):

    def setUp(self):
        """Set up a mock workbook and worksheet for each test."""
        self.workbook = Workbook()
        self.worksheet = self.workbook.active

    def test_write_work_name_row_no_fill(self):
        """Test that the 'Work Name' row has no fill pattern."""
        work_description_data = {'description': 'Test Work'}
        current_row = 1
        
        # Call the function to write the work name row
        write_work_name_row(self.worksheet, work_description_data, current_row)
        
        # Get the cell that was written to
        cell = self.worksheet.cell(row=current_row, column=1)
        
        # Assert that the fill pattern is None
        self.assertIsNone(cell.fill.patternType, "The 'Work Name' cell should have no fill.")

    def test_allocation_code_for_mp(self):
        """Test that the correct allocation code is set for M&P subcategory."""
        with patch.object(self.worksheet, 'cell', return_value=MagicMock()) as mock_cell:
            write_summary_section(self.worksheet, 2, 10, work_subcategory='M&P')
            
            # Find the call for the allocation code
            allocation_call = None
            for call in mock_cell.call_args_list:
                if 'value' in call.kwargs and 'Allocation' in call.kwargs['value']:
                    allocation_call = call
                    break
            
            self.assertIsNotNone(allocation_call, "Allocation cell was not written.")
            self.assertIn('47000 050 443 32', allocation_call.kwargs['value'])

    def test_allocation_code_for_rsp(self):
        """Test that the correct allocation code is set for RSP subcategory."""
        with patch.object(self.worksheet, 'cell', return_value=MagicMock()) as mock_cell:
            write_summary_section(self.worksheet, 2, 10, work_subcategory='RSP')
            
            # Find the call for the allocation code
            allocation_call = None
            for call in mock_cell.call_args_list:
                if 'value' in call.kwargs and 'Allocation' in call.kwargs['value']:
                    allocation_call = call
                    break
            
            self.assertIsNotNone(allocation_call, "Allocation cell was not written.")
            self.assertIn('47000 070 443 32', allocation_call.kwargs['value'])

    def test_allocation_code_for_default(self):
        """Test that the correct allocation code is set for default (None/other) subcategory."""
        with patch.object(self.worksheet, 'cell', return_value=MagicMock()) as mock_cell:
            write_summary_section(self.worksheet, 2, 10, work_subcategory=None)
            
            # Find the call for the allocation code
            allocation_call = None
            for call in mock_cell.call_args_list:
                if 'value' in call.kwargs and 'Allocation' in call.kwargs['value']:
                    allocation_call = call
                    break
            
            self.assertIsNotNone(allocation_call, "Allocation cell was not written.")
            self.assertIn('47000 070 443 32', allocation_call.kwargs['value'])

if __name__ == '__main__':
    unittest.main()

