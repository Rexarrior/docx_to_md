from typing import List, Optional
from .paragraph import Paragraph

class Document:
    """
    Represents a document containing paragraphs, images, and tables.
    Acts as a container for the document structure.
    """
    
    def __init__(self):
        self.paragraphs: List[Paragraph] = []
        self.title: str = ""
        self.filename: str = ""
        self.image_count: int = 0
        
    def add_paragraph(self, paragraph: Paragraph) -> None:
        """Add a paragraph to the document"""
        pass
    
    def get_images(self) -> List:
        """Get all images in the document"""
        pass
    
    def get_tables(self) -> List:
        """Get all tables in the document"""
        pass 