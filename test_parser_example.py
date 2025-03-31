"""
Test script to parse the example document and analyze the output.
"""
import os
from src.parser.docx_parser import DocxParser
from src.models.document import Document
from src.models.paragraph import Paragraph
from src.models.image import Image
from src.models.table import Table

def main():
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
    print(f"Paragraphs: {len(document.paragraphs)}")
    
    # Count headings, images, and tables
    heading_count = 0
    image_count = 0
    table_count = 0
    
    for paragraph in document.paragraphs:
        if paragraph.is_heading():
            heading_count += 1
        if paragraph.has_image():
            image_count += 1
        if paragraph.has_table():
            table_count += 1
    
    print(f"Headings: {heading_count}")
    print(f"Images: {image_count}")
    print(f"Tables: {table_count}")
    
    # Print the first 10 paragraphs with their information
    print("\nSample paragraphs:")
    for i, paragraph in enumerate(document.paragraphs[:10]):
        print(f"\nParagraph {i+1}:")
        print(f"  Text: {paragraph.text[:50]}...")
        print(f"  Heading: {'Yes' if paragraph.is_heading() else 'No'}")
        if paragraph.is_heading():
            print(f"  Heading level: {paragraph.heading_level}")
        print(f"  Has image: {'Yes' if paragraph.has_image() else 'No'}")
        print(f"  Has table: {'Yes' if paragraph.has_table() else 'No'}")
        print(f"  Text runs: {len(paragraph.runs)}")
        
        # Print the first few runs if they exist
        if paragraph.runs:
            print("  Sample runs:")
            for j, run in enumerate(paragraph.runs[:3]):
                formatting = []
                if run.get('bold', False): formatting.append('bold')
                if run.get('italic', False): formatting.append('italic')
                if run.get('underline', False): formatting.append('underline')
                if run.get('strike', False): formatting.append('strikethrough')
                
                print(f"    Run {j+1}: '{run['text'][:20]}...' - {', '.join(formatting) or 'plain'}")

if __name__ == "__main__":
    main() 