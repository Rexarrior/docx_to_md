#!/usr/bin/env python
"""
Word to Markdown Converter

This script converts Microsoft Word (.docx) documents to Markdown format.
It preserves formatting, extracts images, and converts tables.
"""
import os
import sys
import argparse
from src.main import convert_docx_to_markdown


def main():
    """Main entry point for the command-line interface"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Convert Microsoft Word (.docx) files to Markdown format'
    )
    parser.add_argument('input', help='Path to the input .docx file')
    parser.add_argument(
        '-o', '--output',
        help='Directory to save the output files (default: same as input)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_file = args.input
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not input_file.lower().endswith('.docx'):
        print(f"Warning: Input file '{input_file}' doesn't have a .docx extension")
    
    # Convert document
    try:
        output_path = convert_docx_to_markdown(input_file, args.output)
        print(f"Conversion successful! Output saved to: {output_path}")
    except Exception as e:
        print(f"Error during conversion: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 