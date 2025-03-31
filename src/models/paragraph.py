from typing import Dict, Optional, List, Any

class Paragraph:
    """
    Represents a document paragraph with all its content and attributes.
    Can contain text, images, and tables.
    """
    
    def __init__(self):
        self.heading: str = ""          # Heading text (if paragraph is a heading)
        self.heading_level: int = 0     # 0 for regular paragraph, 1-6 for heading levels
        self.text: str = ""             # Text content
        self.image = None               # Optional Image object
        self.table = None               # Optional Table object
        self.formatting: Dict[str, Any] = {}  # Text formatting information
        self.runs: List[Dict[str, Any]] = []  # List of text runs with formatting
        
    def has_image(self) -> bool:
        """Check if the paragraph contains an image"""
        pass
    
    def has_table(self) -> bool:
        """Check if the paragraph contains a table"""
        pass
    
    def is_heading(self) -> bool:
        """Check if the paragraph is a heading"""
        pass
    
    def add_run(self, text: str, formatting: Dict[str, bool]) -> None:
        """Add a text run with formatting information"""
        pass 