# Word to Markdown Converter

A Python tool for converting Microsoft Word (.docx) documents to Markdown format while preserving formatting, images, and tables.

## Features

- Converts Word documents to properly formatted Markdown
- Preserves text formatting (bold, italic, underline, strikethrough)
- Extracts and includes images with proper references
- Converts tables to Markdown format
- Maintains document hierarchy (headings, sections)
- Creates a ZIP archive with the Markdown file and extracted media

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/word-to-md-converter.git
cd word-to-md-converter
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
python docx2md.py input.docx [-o output_directory]
```

Options:
- `input.docx`: Path to the input Word document
- `-o, --output`: Directory to save the output files (default: same as input)

### Python API

```python
from src.main import convert_docx_to_markdown

# Convert a document
zip_path = convert_docx_to_markdown('input.docx', 'output_directory')
print(f"Output saved to: {zip_path}")
```

## Output

The converter produces:

1. A Markdown (.md) file with the same name as the input document
2. A folder containing extracted images
3. A ZIP archive containing both the Markdown file and the images folder

## Formatting Support

- **Headings**: Converted to proper Markdown headings
- **Bold**: Converted to `**bold**`
- **Italic**: Converted to `*italic*`
- **Underline**: Converted to `__underlined__`
- **Strikethrough**: Converted to `~~strikethrough~~`
- **Images**: Extracted and referenced with `![alt_text](image_name.png)`
- **Tables**: Converted to Markdown tables with proper alignment

## Requirements

- Python 3.6+
- python-docx
- Pillow

## License

[MIT License](LICENSE) 