from typing import List, Dict, Any, Optional

class Table:
    """
    Representation of a table structure.
    Contains rows, cells, and formatting information.
    """
    
    def __init__(self):
        self.rows: List[List[str]] = []  # List of rows, each containing cell values
        self.header: bool = False        # Whether the first row is a header
        self.num_rows: int = 0           # Number of rows
        self.num_cols: int = 0           # Number of columns
        self.column_alignments: List[str] = []  # Alignment for each column ('left', 'center', 'right')
        self.caption: str = ""           # Optional table caption
        
    def add_row(self, row: List[str]) -> None:
        """Add a row to the table"""
        self.rows.append(row)
        self.num_rows = len(self.rows)
        
        # Update number of columns if necessary
        if len(row) > self.num_cols:
            self.num_cols = len(row)
            # Extend column_alignments if needed
            while len(self.column_alignments) < self.num_cols:
                self.column_alignments.append('left')
    
    def set_column_alignment(self, col_index: int, alignment: str) -> None:
        """Set the alignment for a specific column"""
        if alignment not in ('left', 'center', 'right'):
            raise ValueError("Alignment must be 'left', 'center', or 'right'")
            
        # Ensure we have enough alignment entries
        while len(self.column_alignments) <= col_index:
            self.column_alignments.append('left')
            
        self.column_alignments[col_index] = alignment
    
    def get_markdown(self) -> str:
        """
        Convert the table to Markdown format
        
        Returns:
            str: Markdown representation of the table
        """
        if not self.rows or self.num_cols == 0:
            return ""
            
        md_lines = []
        
        # Build header row
        header_row = '|'
        for cell in self.rows[0]:
            header_row += f" {cell} |"
        md_lines.append(header_row)
        
        # Build separator row with alignment indicators
        separator_row = '|'
        for i in range(self.num_cols):
            alignment = self.column_alignments[i] if i < len(self.column_alignments) else 'left'
            if alignment == 'left':
                separator_row += " :- |"
            elif alignment == 'center':
                separator_row += " :-: |"
            elif alignment == 'right':
                separator_row += " -: |"
        md_lines.append(separator_row)
        
        # Build data rows
        for row in self.rows[1:]:
            data_row = '|'
            for cell in row:
                data_row += f" {cell} |"
            md_lines.append(data_row)
            
        return '\n'.join(md_lines) 