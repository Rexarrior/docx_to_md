# Word-to-Markdown Converter Architecture

## Overview

The Word-to-Markdown converter follows a clean, modular architecture with clear separation of concerns. The system is designed around three primary components:

1. **Parser**: Responsible for extracting content from DOCX files
2. **Document Model**: Data structures that represent the document content
3. **Markdown Writer**: Converts the document model to properly formatted Markdown

## Component Diagram

```
┌────────────┐    ┌─────────────────┐    ┌────────────────┐    ┌─────────────┐
│ DOCX File  │───▶│ DocxParser      │───▶│ Document Model │───▶│ MarkdownWriter │───▶ Markdown + ZIP
└────────────┘    └─────────────────┘    └────────────────┘    └─────────────┘
```

## Document Model

### Document
A container for the entire document structure.

```python
class Document:
    def __init__(self):
        self.paragraphs = []  # List of Paragraph objects
        self.title = ""       # Document title
```

### Paragraph
Represents a document paragraph with all its content and attributes.

```python
class Paragraph:
    def __init__(self):
        self.heading = ""          # Heading text (if paragraph is a heading)
        self.heading_level = 0     # 0 for regular paragraph, 1-6 for heading levels
        self.text = ""             # Text content
        self.image = None          # Optional Image object
        self.table = None          # Optional Table object
        self.formatting = {}       # Text formatting information
```

### Image
Container for image data and metadata.

```python
class Image:
    def __init__(self):
        self.file_path = ""        # Original path in the docx
        self.content = None        # Binary content of the image
        self.new_file_name = ""    # Generated filename for the output
```

### Table
Representation of a table structure.

```python
class Table:
    def __init__(self):
        self.rows = []             # List of rows
        self.header = False        # Whether the first row is a header
```

## Parser Component

The DocxParser encapsulates all logic for reading and parsing Word documents.

```python
class DocxParser:
    def __init__(self):
        self.image_counter = 1     # Counter for generating image filenames
    
    def parse_document(self, docx_path):
        """
        Parse a DOCX file and return a Document object.
        
        Args:
            docx_path (str): Path to the DOCX file
            
        Returns:
            Document: Parsed document object
        """
        # Implementation details
        pass
        
    def _parse_paragraph(self, paragraph):
        """Parse a paragraph element from docx"""
        pass
        
    def _extract_image(self, run):
        """Extract image from a run element"""
        pass
        
    def _parse_table(self, table):
        """Parse a table element from docx"""
        pass
```

## Markdown Writer Component

The MarkdownWriter handles the conversion from the document model to Markdown format.

```python
class MarkdownWriter:
    def __init__(self):
        pass
    
    def write_document(self, document, output_path):
        """
        Convert a Document object to Markdown and write to the specified path.
        
        Args:
            document (Document): Document object to convert
            output_path (str): Path where to write the output
            
        Returns:
            str: Path to the generated Markdown file
        """
        # Generate Markdown content
        # Extract and save images
        # Create markdown file
        # Create zip archive
        pass
        
    def _format_paragraph(self, paragraph):
        """Convert a Paragraph object to Markdown syntax"""
        pass
        
    def _format_image(self, image, document_name):
        """Process an Image object and return Markdown reference"""
        pass
        
    def _format_table(self, table):
        """Convert a Table object to Markdown table syntax"""
        pass
        
    def _create_zip_archive(self, md_file_path, media_folder_path):
        """Create a ZIP archive with the Markdown file and media folder"""
        pass
```

## Processing Flow

1. **Initialization**:
   - DocxParser is initialized
   - Document path is provided

2. **Parsing**:
   - DocxParser reads the DOCX file
   - Content is extracted and organized into Document, Paragraph, Image, and Table objects
   - Document object is populated with structured content

3. **Markdown Generation**:
   - MarkdownWriter receives the Document object
   - Each element is converted to appropriate Markdown syntax
   - Images are extracted and saved
   - Tables are formatted according to Markdown table syntax
   - Formatting is applied (bold, italic, etc.)

4. **Output Creation**:
   - Markdown file is written to disk
   - Media folder is created with extracted images
   - ZIP archive is created containing both the Markdown file and media folder

## Design Considerations

1. **Modularity**: Each component has a single responsibility, making the system easier to maintain and extend.

2. **Separation of Concerns**: 
   - Parsing logic is isolated from Markdown generation
   - Document model provides a clean interface between components

3. **Extensibility**:
   - New document elements can be added by extending the model
   - Different parsers or writers could be implemented for other formats

4. **Error Handling**:
   - Each component includes appropriate error handling
   - Parsing errors shouldn't stop the entire process
   - Unsupported elements are handled gracefully

## Implementation Strategy

1. Implement the base document model classes
2. Create the DocxParser with basic paragraph and text extraction
3. Implement the MarkdownWriter with basic formatting support
4. Add image extraction and handling
5. Implement table conversion
6. Add support for complex formatting
7. Create the archive generation functionality
8. Implement error handling and logging
9. Add command-line interface 