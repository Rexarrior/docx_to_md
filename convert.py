#!/usr/bin/env python
"""
Script to convert Word documents to Markdown with custom formatting.
Usage: python convert.py input.docx [output_directory]
"""
import os
import sys
from src.parser.docx_parser import DocxParser
from src.writer.markdown_writer import MarkdownWriter

def main():
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python convert.py input.docx [output_directory]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Set output directory (default is current directory)
    output_dir = os.getcwd()
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    # Verify input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get output filename (without extension)
    output_base = os.path.splitext(os.path.basename(input_file))[0]
    output_path = os.path.join(output_dir, output_base)
    
    print(f"Converting '{input_file}' to Markdown...")
    
    try:
        # Parse the document
        parser = DocxParser()
        document = parser.parse_document(input_file)
        
        # Write to Markdown
        writer = MarkdownWriter()
        zip_path = writer.write_document(document, output_path)
        
        md_file = f"{output_path}.md"
        
        print(f"\nConversion successful!")
        print(f"Markdown file: {md_file}")
        print(f"ZIP archive: {zip_path}")
        
        # Print some statistics
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            heading_count = sum(1 for line in lines if line.strip().startswith('-'))
            image_count = sum(1 for line in lines if '![' in line and '](' in line)
            table_count = sum(1 for line in lines if line.strip().startswith('|'))
        
        print(f"\nStatistics:")
        print(f"- Total lines: {len(lines)}")
        print(f"- Headings: {heading_count}")
        print(f"- Images: {image_count}")
        print(f"- Table rows: {table_count}")
        
    except Exception as e:
        print(f"\nError during conversion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 