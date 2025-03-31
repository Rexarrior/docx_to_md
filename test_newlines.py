#!/usr/bin/env python
"""
Test script to verify that newlines in paragraph text are handled correctly.
Creates test paragraphs with newlines and generates markdown to check indentation.
"""
import os
import sys
from src.models.document import Document
from src.models.paragraph import Paragraph
from src.writer.markdown_writer import MarkdownWriter

def main():
    # Create output directory
    output_dir = "test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Testing newline handling in paragraph text...")
    
    # Create a test document with paragraphs containing newlines
    document = Document()
    document.filename = "test_newlines.docx"
    
    # Add a level 1 heading
    h1 = Paragraph()
    h1.heading_level = 1
    h1.text = "Main Heading"
    document.add_paragraph(h1)
    
    # Add a paragraph with newlines under the heading
    p1 = Paragraph()
    p1.text = "This is a paragraph with\nnewlines that should be\nproperly indented."
    document.add_paragraph(p1)
    
    # Add a level 2 heading
    h2 = Paragraph()
    h2.heading_level = 2
    h2.text = "Subheading"
    document.add_paragraph(h2)
    
    # Add a paragraph with newlines under the subheading
    p2 = Paragraph()
    p2.text = "This is another paragraph with\nnewlines under a level 2 heading.\nIt should have more indentation."
    document.add_paragraph(p2)
    
    # Add a level 3 heading
    h3 = Paragraph()
    h3.heading_level = 3
    h3.text = "Sub-subheading"
    document.add_paragraph(h3)
    
    # Add a paragraph with newlines and formatting
    p3 = Paragraph()
    p3.text = "This paragraph has\nnewlines and will have\nformatting applied."
    # Add formatted runs
    p3.runs = [
        {"text": "This paragraph has", "bold": True, "italic": False, "underline": False, "strike": False},
        {"text": "\nnewlines and will have", "bold": False, "italic": True, "underline": False, "strike": False},
        {"text": "\nformatting applied.", "bold": False, "italic": False, "underline": True, "strike": False},
    ]
    document.add_paragraph(p3)
    
    # Add a bulleted list with newlines
    bullet_list = Paragraph()
    bullet_list.text = "- First bullet point\n- Second bullet point with\n  continuation\n- Third bullet point"
    document.add_paragraph(bullet_list)
    
    # Create writer and write the document
    writer = MarkdownWriter()
    output_path = os.path.join(output_dir, "newline_test")
    zip_path = writer.write_document(document, output_path)
    
    # Read and display the generated Markdown
    md_file_path = f"{output_path}.md"
    
    if os.path.exists(md_file_path):
        print(f"\nGenerated Markdown file: {md_file_path}")
        print("Content of the generated Markdown file:")
        print("-" * 50)
        
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        
        print("-" * 50)
        print("Checking for proper indentation after newlines...")
        
        # Count lines and check indentation
        lines = content.split('\n')
        indented_newlines = 0
        
        for i, line in enumerate(lines):
            if i > 0 and line.strip() and lines[i-1].strip() and not lines[i-1].endswith('\\'):
                # This might be a continued line from a newline in the original text
                if line.startswith('\t'):
                    indented_newlines += 1
        
        print(f"Found {indented_newlines} properly indented continued lines.")
        print("Test complete!")
    else:
        print(f"Error: Generated Markdown file not found: {md_file_path}")

if __name__ == "__main__":
    main() 