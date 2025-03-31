#!/usr/bin/env python
"""
Test script to verify heading level detection and conversion.
Parses a Word document and shows the heading level detected for each paragraph.
"""
import os
import sys
import re
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
    
    print(f"Testing heading level detection on {example_docx}")
    
    # Create an output directory for test results
    output_dir = "test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Parse the document
    parser = DocxParser()
    document = parser.parse_document(example_docx)
    
    # Print document information
    print(f"Document: {document.filename}")
    print(f"Total Paragraphs: {len(document.paragraphs)}")
    
    # Count headings by level
    heading_levels = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    all_headings = []
    
    for paragraph in document.paragraphs:
        if paragraph.is_heading():
            level = paragraph.heading_level
            heading_levels[level] = heading_levels.get(level, 0) + 1
            all_headings.append((level, paragraph.text))
    
    # Print heading level statistics
    print("\nHeading Level Distribution:")
    for level, count in heading_levels.items():
        if count > 0:
            print(f"  Level {level}: {count} headings")
    
    # Print the first few headings of each level
    print("\nSample Headings by Level:")
    for level in range(1, 7):
        samples = [h[1] for h in all_headings if h[0] == level][:3]  # Take up to 3 examples
        if samples:
            print(f"  Level {level} examples:")
            for sample in samples:
                preview = sample[:50] + "..." if len(sample) > 50 else sample
                print(f"    - {preview}")
    
    # Create a MarkdownWriter and convert the document
    writer = MarkdownWriter()
    output_path = os.path.join(output_dir, "heading_test")
    writer.write_document(document, output_path)
    
    # Read the generated Markdown file to verify heading levels
    md_file_path = f"{output_path}.md"
    
    print(f"\nAnalyzing Markdown output at {md_file_path}")
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Count actual heading levels in the Markdown output
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    md_headings = heading_pattern.findall(md_content)
    
    md_heading_levels = {}
    for heading in md_headings:
        level = len(heading[0])  # Count the # characters
        md_heading_levels[level] = md_heading_levels.get(level, 0) + 1
    
    print("\nMarkdown Heading Level Distribution:")
    for level, count in sorted(md_heading_levels.items()):
        print(f"  Level {level} (#{level}): {count} headings")
    
    # Print the first few markdown headings
    print("\nSample Markdown Headings:")
    for i, heading in enumerate(md_headings[:10]):  # Show first 10 headings
        level = len(heading[0])
        text = heading[1]
        preview = text[:50] + "..." if len(text) > 50 else text
        print(f"  {i+1}. {'#' * level} {preview}")
    
    print(f"\nTest complete! Full results available at: {md_file_path}")

if __name__ == "__main__":
    main() 