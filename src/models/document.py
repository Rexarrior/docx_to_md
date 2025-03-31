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
        self.paragraphs.append(paragraph)
    
    def get_images(self) -> List:
        """Get all images in the document"""
        images = []
        for paragraph in self.paragraphs:
            if paragraph.image is not None:
                images.append(paragraph.image)
        return images
    
    def get_tables(self) -> List:
        """Get all tables in the document"""
        tables = []
        for paragraph in self.paragraphs:
            if paragraph.table is not None:
                tables.append(paragraph.table)
        return tables 