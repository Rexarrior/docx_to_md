import os
import pytest
from docx import Document as DocxDocument
from unittest.mock import MagicMock, patch

from src.parser.docx_parser import DocxParser
from src.models.document import Document
from src.models.paragraph import Paragraph
from src.models.image import Image
from src.models.table import Table

# Path to the example docx file
EXAMPLE_DOCX = os.path.join('docs', 'example_min.docx')

class TestDocxParser:
    """Tests for the DocxParser class"""
    
    def setup_method(self):
        """Setup before each test method"""
        self.parser = DocxParser()
        
    def test_parser_initialization(self):
        """Test if the parser initializes correctly"""
        assert self.parser.image_counter == 1
        assert self.parser.document is None
        assert self.parser.docx is None
        
    def test_parse_document_creates_document_instance(self):
        """Test if parse_document creates a Document instance"""
        # Skip if the example document doesn't exist
        if not os.path.exists(EXAMPLE_DOCX):
            pytest.skip(f"Example file {EXAMPLE_DOCX} not found")
            
        document = self.parser.parse_document(EXAMPLE_DOCX)
        
        assert isinstance(document, Document)
        assert len(document.paragraphs) > 0
        assert document.filename == os.path.basename(EXAMPLE_DOCX)
        
    def test_detect_heading_level_from_bold_text(self):
        """Test if heading level is detected from bold text"""
        # Create a mock paragraph with bold text
        mock_paragraph = MagicMock()
        mock_run = MagicMock()
        mock_run.bold = True
        mock_run.text = "Heading text"
        mock_paragraph.runs = [mock_run]
        mock_paragraph.text = "Heading text"
        
        heading_level = self.parser._detect_heading_level(mock_paragraph)
        
        # According to our analysis, bold paragraphs are treated as headings
        assert heading_level > 0
        
    def test_detect_heading_level_from_normal_text(self):
        """Test if normal text is not detected as heading"""
        # Create a mock paragraph with normal text
        mock_paragraph = MagicMock()
        mock_run = MagicMock()
        mock_run.bold = False
        mock_run.text = "Normal text"
        mock_paragraph.runs = [mock_run]
        mock_paragraph.text = "Normal text"
        
        # Add style mock
        mock_style = MagicMock()
        mock_style.name = "Normal"
        mock_paragraph.style = mock_style
        
        heading_level = self.parser._detect_heading_level(mock_paragraph)
        
        assert heading_level == 0
        
    def test_parse_paragraph_with_text(self):
        """Test parsing a paragraph with text"""
        # Create a mock docx paragraph with text
        mock_docx_paragraph = MagicMock()
        mock_run = MagicMock()
        mock_run.bold = False
        mock_run.italic = False
        mock_run.underline = False
        mock_run.font.strike = False
        mock_run.text = "Sample text"
        mock_docx_paragraph.runs = [mock_run]
        mock_docx_paragraph.text = "Sample text"
        
        # Need to mock _extract_image and _detect_heading_level
        self.parser._extract_image = MagicMock(return_value=None)
        self.parser._detect_heading_level = MagicMock(return_value=0)
        
        paragraph = self.parser._parse_paragraph(mock_docx_paragraph)
        
        assert isinstance(paragraph, Paragraph)
        assert paragraph.text == "Sample text"
        assert paragraph.heading_level == 0
        assert paragraph.image is None
        
    def test_parse_paragraph_with_formatting(self):
        """Test parsing a paragraph with formatted text"""
        # Create a mock docx paragraph with formatted text
        mock_docx_paragraph = MagicMock()
        
        # Bold run
        mock_bold_run = MagicMock()
        mock_bold_run.bold = True
        mock_bold_run.italic = False
        mock_bold_run.underline = False
        mock_bold_run.font.strike = False
        mock_bold_run.text = "Bold "
        
        # Italic run
        mock_italic_run = MagicMock()
        mock_italic_run.bold = False
        mock_italic_run.italic = True
        mock_italic_run.underline = False
        mock_italic_run.font.strike = False
        mock_italic_run.text = "Italic "
        
        # Regular run
        mock_regular_run = MagicMock()
        mock_regular_run.bold = False
        mock_regular_run.italic = False
        mock_regular_run.underline = False
        mock_regular_run.font.strike = False
        mock_regular_run.text = "Regular"
        
        mock_docx_paragraph.runs = [mock_bold_run, mock_italic_run, mock_regular_run]
        mock_docx_paragraph.text = "Bold Italic Regular"
        
        # Need to mock _extract_image and _detect_heading_level
        self.parser._extract_image = MagicMock(return_value=None)
        self.parser._detect_heading_level = MagicMock(return_value=0)
        self.parser._extract_text_formatting = MagicMock(return_value=[
            {"text": "Bold ", "bold": True, "italic": False, "underline": False, "strike": False},
            {"text": "Italic ", "bold": False, "italic": True, "underline": False, "strike": False},
            {"text": "Regular", "bold": False, "italic": False, "underline": False, "strike": False}
        ])
        
        paragraph = self.parser._parse_paragraph(mock_docx_paragraph)
        
        assert isinstance(paragraph, Paragraph)
        assert paragraph.text == "Bold Italic Regular"
        assert len(paragraph.runs) == 3
        
    def test_extract_image_from_paragraph(self):
        """Test extracting an image from a paragraph"""
        # For this test, we'll need to mock the paragraph and the relationships
        mock_paragraph = MagicMock()
        
        # Create a mock relationship that represents an image
        mock_rel = MagicMock()
        mock_rel.target_ref = "media/image1.png"
        
        # Mock the part and relationships
        mock_part = MagicMock()
        mock_part.rels = {"rId1": mock_rel}
        
        # Mock the blob data
        mock_part.blob = b"fake image data"
        
        # Mock the paragraph's part.related_parts
        mock_paragraph.part.related_parts = {"rId1": mock_part}
        
        # Mock the paragraph's _element.xpath to return a list with one item
        mock_xpath_result = [MagicMock()]
        mock_xpath_result[0].get.return_value = "rId1"
        mock_paragraph._element.xpath.return_value = mock_xpath_result
        
        # Now we can test the _extract_image method
        with patch('src.parser.docx_parser.Image') as MockImage:
            # Set up the mock image instance
            mock_image_instance = MagicMock()
            MockImage.return_value = mock_image_instance
            
            image = self.parser._extract_image(mock_paragraph)
            
            # Assert that the image was created
            assert image is mock_image_instance
            MockImage.assert_called_once()
            
    def test_parse_table(self):
        """Test parsing a table"""
        # Create a mock docx table
        mock_table = MagicMock()
        
        # Create mock rows and cells
        mock_row1 = MagicMock()
        mock_cell1_1 = MagicMock()
        mock_cell1_1.text = "Cell 1,1"
        mock_cell1_2 = MagicMock()
        mock_cell1_2.text = "Cell 1,2"
        mock_row1.cells = [mock_cell1_1, mock_cell1_2]
        
        mock_row2 = MagicMock()
        mock_cell2_1 = MagicMock()
        mock_cell2_1.text = "Cell 2,1"
        mock_cell2_2 = MagicMock()
        mock_cell2_2.text = "Cell 2,2"
        mock_row2.cells = [mock_cell2_1, mock_cell2_2]
        
        mock_table.rows = [mock_row1, mock_row2]
        
        table = self.parser._parse_table(mock_table)
        
        assert isinstance(table, Table)
        assert table.num_rows == 2
        assert table.num_cols == 2
        assert table.rows[0][0] == "Cell 1,1"
        assert table.rows[0][1] == "Cell 1,2"
        assert table.rows[1][0] == "Cell 2,1"
        assert table.rows[1][1] == "Cell 2,2"
        
    def test_extract_text_formatting(self):
        """Test extracting text formatting from a paragraph"""
        # Create a mock docx paragraph with formatted text
        mock_paragraph = MagicMock()
        
        # Bold run
        mock_bold_run = MagicMock()
        mock_bold_run.bold = True
        mock_bold_run.italic = False
        mock_bold_run.underline = False
        mock_bold_run.font.strike = False
        mock_bold_run.text = "Bold"
        
        # Italic run
        mock_italic_run = MagicMock()
        mock_italic_run.bold = False
        mock_italic_run.italic = True
        mock_italic_run.underline = False
        mock_italic_run.font.strike = False
        mock_italic_run.text = "Italic"
        
        mock_paragraph.runs = [mock_bold_run, mock_italic_run]
        
        formatting = self.parser._extract_text_formatting(mock_paragraph)
        
        assert len(formatting) == 2
        assert formatting[0]["text"] == "Bold"
        assert formatting[0]["bold"] is True
        assert formatting[0]["italic"] is False
        assert formatting[1]["text"] == "Italic"
        assert formatting[1]["bold"] is False
        assert formatting[1]["italic"] is True 