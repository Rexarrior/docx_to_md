"""
Test script to parse the example document and analyze the output.
Shows all paragraphs in the document with their information.
"""
import os
import sys
from src.parser.docx_parser import DocxParser
from src.models.document import Document
from src.models.paragraph import Paragraph
from src.models.image import Image
from src.models.table import Table

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
    
    # Parse the document
    parser = DocxParser()
    document = parser.parse_document(example_docx)
    
    # Print document information
    print(f"Document: {document.filename}")
    print(f"Total Paragraphs: {len(document.paragraphs)}")
    
    # Count headings, images, and tables
    heading_count = 0
    image_count = 0
    table_count = 0
    empty_paragraphs = 0
    
    for paragraph in document.paragraphs:
        if paragraph.is_heading():
            heading_count += 1
        if paragraph.has_image():
            image_count += 1
        if paragraph.has_table():
            table_count += 1
        if not paragraph.text.strip() and not paragraph.has_image() and not paragraph.has_table():
            empty_paragraphs += 1
    
    print(f"Headings: {heading_count}")
    print(f"Images: {image_count}")
    print(f"Tables: {table_count}")
    print(f"Empty paragraphs: {empty_paragraphs}")
    
    # Print summary of headings
    print("\nHeadings Summary:")
    heading_number = 1
    for i, paragraph in enumerate(document.paragraphs):
        if paragraph.is_heading():
            text_preview = paragraph.text[:50] + "..." if len(paragraph.text) > 50 else paragraph.text
            print(f"  Heading {heading_number}: {text_preview}")
            heading_number += 1
    
    # Print summary of images
    print("\nImages Summary:")
    image_number = 1
    for i, paragraph in enumerate(document.paragraphs):
        if paragraph.has_image():
            print(f"  Image {image_number}: {paragraph.image.new_file_name}")
            image_number += 1
    
    # Print summary of tables
    print("\nTables Summary:")
    table_number = 1
    for i, paragraph in enumerate(document.paragraphs):
        if paragraph.has_table():
            print(f"  Table {table_number}: {paragraph.table.num_rows} rows x {paragraph.table.num_cols} columns")
            table_number += 1
    
    # Print all paragraphs with their information
    print("\nAll paragraphs:")
    for i, paragraph in enumerate(document.paragraphs):
        print(f"\nParagraph {i+1}:")
        
        # Print text (limited to 50 chars for readability)
        if paragraph.text:
            text_preview = paragraph.text[:50] + "..." if len(paragraph.text) > 50 else paragraph.text
            print(f"  Text: {text_preview}")
        else:
            print("  Text: [empty]")
        
        # Print heading information
        print(f"  Heading: {'Yes' if paragraph.is_heading() else 'No'}")
        if paragraph.is_heading():
            print(f"  Heading level: {paragraph.heading_level}")
        
        # Print image and table information
        print(f"  Has image: {'Yes' if paragraph.has_image() else 'No'}")
        if paragraph.has_image():
            print(f"  Image filename: {paragraph.image.new_file_name}")
            
        print(f"  Has table: {'Yes' if paragraph.has_table() else 'No'}")
        if paragraph.has_table():
            print(f"  Table rows: {paragraph.table.num_rows}, columns: {paragraph.table.num_cols}")
        
        # Print text formatting information
        print(f"  Text runs: {len(paragraph.runs)}")
        
        # Print the first few runs if they exist
        if paragraph.runs:
            for j, run in enumerate(paragraph.runs[:2]):  # Limit to 2 runs for brevity
                formatting = []
                if run.get('bold', False): formatting.append('bold')
                if run.get('italic', False): formatting.append('italic')
                if run.get('underline', False): formatting.append('underline')
                if run.get('strike', False): formatting.append('strikethrough')
                
                run_text = run['text'][:20] + "..." if len(run['text']) > 20 else run['text']
                print(f"    Run {j+1}: '{run_text}' - {', '.join(formatting) or 'plain'}")

if __name__ == "__main__":
    main() 