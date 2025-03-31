"""
Test script to verify the MarkdownWriter implementation.
Takes a parsed document and generates Markdown output.
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
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_output')
    if os.path.exists(output_dir):
        # Clean up previous test output
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    print(f"Parsing document: {example_docx}")
    
    # Parse the document
    parser = DocxParser()
    document = parser.parse_document(example_docx)
    
    print(f"Document parsed successfully")
    print(f"Total Paragraphs: {len(document.paragraphs)}")
    print(f"Images: {len(document.get_images())}")
    print(f"Tables: {len(document.get_tables())}")
    
    print("\nGenerating Markdown...")
    
    # Create writer and write the document
    writer = MarkdownWriter()
    output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(example_docx))[0])
    zip_path = writer.write_document(document, output_path)
    
    print(f"\nMarkdown generated successfully!")
    print(f"Markdown file: {output_path}.md")
    print(f"ZIP archive: {zip_path}")
    
    # Get some stats
    md_file = f"{output_path}.md"
    media_folder = f"{output_path}_media"
    
    print("\nOutput statistics:")
    print(f"Markdown file size: {os.path.getsize(md_file) / 1024:.2f} KB")
    
    if os.path.exists(media_folder):
        image_count = len([f for f in os.listdir(media_folder) if os.path.isfile(os.path.join(media_folder, f))])
        print(f"Media files extracted: {image_count}")
    
    # Print some content from the Markdown file
    print("\nMarkdown file preview (first 20 lines):")
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        preview_lines = lines[:min(20, len(lines))]
        print("".join(preview_lines))
    
    print(f"\nFull output available at: {output_dir}")

if __name__ == "__main__":
    main() 