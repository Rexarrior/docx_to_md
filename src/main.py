#!/usr/bin/env python
import os
import argparse
import sys
from typing import Optional

from .parser import DocxParser
from .writer import MarkdownWriter


def convert_docx_to_markdown(input_file: str, output_dir: Optional[str] = None) -> str:
    """
    Convert a DOCX file to Markdown format
    
    Args:
        input_file: Path to the input DOCX file
        output_dir: Optional directory to save output files (default: same as input)
        
    Returns:
        str: Path to the generated ZIP archive
    """
    # Get output directory
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(input_file))
    
    # Create parser and writer
    parser = DocxParser()
    writer = MarkdownWriter()
    
    # Parse document
    document = parser.parse_document(input_file)
    
    # Write markdown file
    output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0])
    zip_path = writer.write_document(document, output_path)
    
    return zip_path


def main():
    """CLI entry point for the converter"""
    # Create argument parser
    parser = argparse.ArgumentParser(description='Convert DOCX files to Markdown format')
    parser.add_argument('input', help='Path to the input DOCX file')
    parser.add_argument('-o', '--output', help='Directory to save output files')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Convert document
    try:
        output_path = convert_docx_to_markdown(args.input, args.output)
        print(f"Conversion successful! Output saved to: {output_path}")
    except Exception as e:
        print(f"Error during conversion: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 