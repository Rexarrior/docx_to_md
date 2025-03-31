#!/usr/bin/env python
"""
Test script to verify the new markdown formatting with tabs and dashes.
Parses a Word document and generates Markdown with the updated formatting.
"""
import os
import sys
import shutil
from src.parser.docx_parser import DocxParser
from src.writer.markdown_writer import MarkdownWriter

def main():
    # Set console encoding to UTF-8
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            # Python < 3.7 doesn't have reconfigure
            print("Warning: Console encoding may not display characters correctly")
    
    # Path to the example document
    example_docx = os.path.join('docs', 'example_min.docx')
    
    if not os.path.exists(example_docx):
        print(f"Error: Example file {example_docx} not found")
        return
    
    # Create output directory
    output_dir = "test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Testing new markdown formatting with tabs and dashes on {example_docx}")
    
    # Parse the document
    parser = DocxParser()
    document = parser.parse_document(example_docx)
    
    # Create writer and write the document with new formatting
    writer = MarkdownWriter()
    output_path = os.path.join(output_dir, "formatted_test")
    zip_path = writer.write_document(document, output_path)
    
    # Read the generated Markdown file
    md_file_path = f"{output_path}.md"
    
    if os.path.exists(md_file_path):
        print(f"\nGenerated Markdown file: {md_file_path}")
        print("Preview of the generated Markdown file:")
        print("-" * 50)
        
        # Read and display the first 30 lines
        with open(md_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:30]):
                print(f"{i+1:2d}: {line}", end='')
        
        print("\n" + "-" * 50)
        
        # Count occurrences of different heading levels
        heading_counts = {level: 0 for level in range(1, 7)}
        dash_count = 0
        tab_count = 0
        
        for line in lines:
            if line.strip().startswith('-'):
                dash_count += 1
                # Count tabs at the beginning of the line
                tab_prefix = ''
                for char in line:
                    if char == '\t':
                        tab_prefix += '\t'
                    else:
                        break
                
                tab_level = len(tab_prefix)
                heading_level = tab_level + 1  # Level 1 has 0 tabs, level 2 has 1 tab, etc.
                
                if 1 <= heading_level <= 6:
                    heading_counts[heading_level] += 1
            
            if '\t' in line:
                tab_count += 1
        
        print("\nFormatting Statistics:")
        print(f"Total lines with tabs: {tab_count}")
        print(f"Total heading lines with dashes: {dash_count}")
        
        print("\nDetected Heading Levels:")
        for level, count in heading_counts.items():
            if count > 0:
                print(f"  Level {level} (with {level-1} tabs): {count} headings")
        
        print(f"\nFull output available at: {md_file_path}")
    else:
        print(f"Error: Generated Markdown file not found: {md_file_path}")

if __name__ == "__main__":
    main() 