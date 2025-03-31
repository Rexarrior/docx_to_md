from typing import Dict, List, Any, Optional, Tuple
import os
from docx import Document as DocxDocument
from docx.document import Document as DocxDocumentClass
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph as DocxParagraph
# from docx.oxml.text.run import CT_R
# from docx.oxml.xmlchemy import OxmlElement

from ..models import Document, Paragraph, Image, Table

class DocxParser:
    """
    Parser for DOCX files.
    Converts DOCX elements into the document model structure.
    """
    
    def __init__(self):
        self.image_counter: int = 1  # Counter for generating image filenames
        self.document: Optional[Document] = None
        self.docx: Optional[DocxDocumentClass] = None
        
    def parse_document(self, docx_path: str) -> Document:
        """
        Parse a DOCX file and return a Document object.
        
        Args:
            docx_path (str): Path to the DOCX file
            
        Returns:
            Document: Parsed document object
        """
        # Create a new document
        self.document = Document()
        self.document.filename = os.path.basename(docx_path)
        
        # Load the docx file
        self.docx = DocxDocument(docx_path)
        
        # Process paragraphs
        for paragraph in self.docx.paragraphs:
            if paragraph.text.strip() or self._has_image(paragraph):
                parsed_paragraph = self._parse_paragraph(paragraph)
                self.document.add_paragraph(parsed_paragraph)
        
        # Process tables
        for table in self.docx.tables:
            parsed_table = self._parse_table(table)
            
            # Create a paragraph for the table
            table_paragraph = Paragraph()
            table_paragraph.table = parsed_table
            
            self.document.add_paragraph(table_paragraph)
        
        return self.document
        
    def _parse_paragraph(self, paragraph: DocxParagraph) -> Paragraph:
        """
        Parse a paragraph element from docx
        
        Args:
            paragraph: A docx paragraph object
            
        Returns:
            Paragraph: The parsed Paragraph object
        """
        model_paragraph = Paragraph()
        
        # Extract text
        model_paragraph.text = paragraph.text
        
        # Detect if it's a heading
        model_paragraph.heading_level = self._detect_heading_level(paragraph)
        if model_paragraph.heading_level > 0:
            model_paragraph.heading = paragraph.text
        
        # Extract formatting
        model_paragraph.runs = self._extract_text_formatting(paragraph)
        
        # Extract image if present
        model_paragraph.image = self._extract_image(paragraph)
        
        return model_paragraph
        
    def _extract_image(self, paragraph: DocxParagraph) -> Optional[Image]:
        """
        Extract image from a paragraph
        
        Args:
            paragraph: A docx paragraph that might contain an image
            
        Returns:
            Optional[Image]: The extracted image or None
        """
        # Check if paragraph contains an image using xpath to find inline shapes
        image_elements = paragraph._element.xpath('.//a:blip')
        if not image_elements:
            return None
        
        # For simplicity, we'll just take the first image
        for element in paragraph._element.xpath('.//a:blip'):
            # Get the relationship ID
            rId = element.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            if rId:
                try:
                    # Get the image part
                    image_part = paragraph.part.related_parts[rId]
                    
                    # Create an Image object
                    image = Image()
                    image.file_path = image_part.partname
                    image.content = image_part.blob
                    
                    # Set alt text if available
                    try:
                        drawing_element = element.getparent().getparent().getparent()
                        doc_pr = drawing_element.xpath('.//wp:docPr', namespaces=drawing_element.nsmap)
                        if doc_pr:
                            image.alt_text = doc_pr[0].get('descr', '')
                        else:
                            image.alt_text = ""
                    except:
                        image.alt_text = ""
                    
                    # Generate a new filename
                    image.new_file_name = f"document.{self.image_counter:03d}.png"
                    self.image_counter += 1
                    
                    return image
                except:
                    # If we can't extract the image, continue to the next one
                    continue
        
        return None
        
    def _parse_table(self, table: DocxTable) -> Table:
        """
        Parse a table element from docx
        
        Args:
            table: A docx table object
            
        Returns:
            Table: The parsed Table object
        """
        model_table = Table()
        
        # Process rows
        for row in table.rows:
            model_row = []
            
            # Process cells
            for cell in row.cells:
                model_row.append(cell.text)
            
            model_table.add_row(model_row)
        
        # The first row is typically a header in markdown
        model_table.header = True
        
        # Set default alignments (left for all columns)
        for i in range(model_table.num_cols):
            model_table.set_column_alignment(i, 'left')
        
        return model_table
    
    def _detect_heading_level(self, paragraph: DocxParagraph) -> int:
        """
        Detect the heading level of a paragraph
        
        Args:
            paragraph: A docx paragraph
            
        Returns:
            int: The heading level (0 for normal paragraphs)
        """
        # Check if it's a heading by style name
        if hasattr(paragraph, 'style') and paragraph.style and paragraph.style.name.startswith('Heading'):
            try:
                # Extract heading level from style name (e.g., 'Heading 1' -> 1)
                return int(paragraph.style.name.split()[-1])
            except:
                # Default to level 1 if we can't extract the level
                return 1
        
        # Check if it's a bold paragraph (our analysis showed that bold paragraphs are treated as headings)
        if paragraph.runs and paragraph.text.strip():
            # If the entire paragraph is bold
            all_text = "".join(run.text for run in paragraph.runs)
            all_bold = True
            
            for run in paragraph.runs:
                if run.text.strip() and not run.bold:
                    all_bold = False
                    break
            
            if all_bold and all_text.strip():
                return 1  # Treat as heading level 1
            
            # If the first run is bold and contains the entire text
            first_run = paragraph.runs[0]
            if first_run.bold and first_run.text.strip() and first_run.text.strip() == paragraph.text.strip():
                return 1  # Treat as heading level 1
        
        return 0  # Not a heading
    
    def _extract_text_formatting(self, paragraph: DocxParagraph) -> List[Dict[str, Any]]:
        """
        Extract text runs with their formatting
        
        Args:
            paragraph: A docx paragraph
            
        Returns:
            List[Dict]: List of runs with text and formatting info
        """
        formatted_runs = []
        
        for run in paragraph.runs:
            if not run.text:
                continue
                
            # Extract formatting attributes
            formatting = {
                "text": run.text,
                "bold": bool(run.bold),
                "italic": bool(run.italic),
                "underline": bool(run.underline),
                "strike": bool(run.font.strike)
            }
            
            formatted_runs.append(formatting)
            
        return formatted_runs
    
    def _has_image(self, paragraph: DocxParagraph) -> bool:
        """
        Check if a paragraph contains an image
        
        Args:
            paragraph: A docx paragraph
            
        Returns:
            bool: True if the paragraph contains an image
        """
        return len(paragraph._element.xpath('.//a:blip')) > 0 