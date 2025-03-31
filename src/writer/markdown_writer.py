import os
import zipfile
from typing import Dict, List, Any, Optional, TextIO
import re

from ..models import Document, Paragraph, Image, Table

class MarkdownWriter:
    """
    Writer for Markdown output.
    Converts the document model to Markdown format and creates the output files.
    """
    
    def __init__(self):
        self.output_dir: str = ""
        self.document: Optional[Document] = None
        self.media_folder: str = ""
        self.md_file_path: str = ""
        self.current_heading_level: int = 0  # Track the current heading level for indentation
        
    def write_document(self, document: Document, output_path: str) -> str:
        """
        Convert a Document object to Markdown and write to the specified path.
        
        Args:
            document (Document): Document object to convert
            output_path (str): Path where to write the output
            
        Returns:
            str: Path to the generated Markdown file
        """
        self.document = document
        self.output_dir = os.path.dirname(output_path)
        self.current_heading_level = 0
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Set up paths
        doc_name = os.path.splitext(os.path.basename(output_path))[0]
        self.md_file_path = f"{output_path}.md"
        self.media_folder = os.path.join(self.output_dir, f"{doc_name}_media")
        
        # Create media folder if it doesn't exist
        if not os.path.exists(self.media_folder):
            os.makedirs(self.media_folder)
        
        # Process images and save them
        self._save_images()
        
        # Generate markdown content
        md_content = self._generate_markdown()
        
        # Write markdown file
        with open(self.md_file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # Create ZIP archive
        zip_path = self._create_zip_archive(self.md_file_path, self.media_folder)
        
        return zip_path
        
    def _format_paragraph(self, paragraph: Paragraph) -> str:
        """
        Convert a Paragraph object to Markdown syntax
        
        Args:
            paragraph: A paragraph object
            
        Returns:
            str: Markdown representation of the paragraph
        """
        # Update the current heading level when encountering a heading
        if paragraph.is_heading():
            self.current_heading_level = paragraph.heading_level
        
        # Determine indentation based on current level
        content_indent = "\t" * self.current_heading_level
        
        # If paragraph has an image, format it
        if paragraph.has_image():
            return content_indent + self._format_image(paragraph.image, os.path.basename(self.output_dir))
        
        # If paragraph has a table, format it
        if paragraph.has_table():
            return self._format_table(paragraph.table, self.current_heading_level)
        
        # If it's a heading, format with appropriate indentation and dash
        if paragraph.is_heading():
            # Level 1 heading gets no tabs, level 2 gets 1 tab, etc.
            heading_indent = "\t" * (paragraph.heading_level - 1) if paragraph.heading_level > 0 else ""
            # Make heading text bold
            return f"{heading_indent}- **{paragraph.text}**\n\n"
        
        # Check if the paragraph text starts with a bullet point or numbered list
        text = paragraph.text.strip()
        if text.startswith("- ") or re.match(r"^\d+\.\s", text):
            # For bullet points and numbered lists that are part of the content, 
            # add one extra tab for proper list formatting
            # Also handle newlines in the text by adding proper indentation after each newline
            indented_text = self._add_indent_after_newlines(text, content_indent)
            return f"{content_indent}{indented_text}\n\n"
        
        # If paragraph has formatted runs, use them with content indentation
        if paragraph.runs:
            formatted_text = self._format_text_with_runs(paragraph)
            # Check for lists in formatted text
            if formatted_text.strip().startswith("- ") or re.match(r"^\d+\.\s", formatted_text.strip()):
                indented_text = self._add_indent_after_newlines(formatted_text, content_indent)
                return f"{content_indent}{indented_text}\n\n"
            else:
                indented_text = self._add_indent_after_newlines(formatted_text, content_indent)
                return f"{content_indent}{indented_text}\n\n"
        
        # Otherwise, just return the text with a double newline and indentation
        if text:
            indented_text = self._add_indent_after_newlines(text, content_indent)
            return f"{content_indent}{indented_text}\n\n"
        
        # Empty paragraph
        return "\n"
        
    def _add_indent_after_newlines(self, text: str, indent: str) -> str:
        """
        Add proper indentation after each newline in the text
        
        Args:
            text: The text to process
            indent: The indentation to add after newlines
            
        Returns:
            str: Text with proper indentation after newlines
        """
        # Skip if there are no newlines
        if '\n' not in text:
            return text
        
        # Split by newline and join with newline + indent
        lines = text.split('\n')
        return '\n'.join([lines[0]] + [f"{indent}{line}" for line in lines[1:]])
        
    def _format_image(self, image: Image, document_name: str) -> str:
        """
        Process an Image object and return Markdown reference
        
        Args:
            image: An Image object
            document_name: Name of the document (for folder name)
            
        Returns:
            str: Markdown image reference
        """
        alt_text = image.alt_text if image.alt_text else "image"
        media_folder_name = f"{os.path.splitext(os.path.basename(self.md_file_path))[0]}_media"
        image_path = f"{media_folder_name}/{image.new_file_name}"
        return f"![{alt_text}]({image_path})\n\n"
        
    def _format_table(self, table: Table, indent_level: int) -> str:
        """
        Convert a Table object to Markdown table syntax with proper indentation
        
        Args:
            table: A Table object
            indent_level: Current indentation level
            
        Returns:
            str: Markdown table representation
        """
        indent = "\t" * indent_level
        
        # Get the basic markdown table
        table_md = table.get_markdown()
        
        # Apply indentation to each line while preserving table format
        indented_lines = []
        for line in table_md.split('\n'):
            indented_lines.append(f"{indent}{line}")
        
        return '\n'.join(indented_lines) + "\n\n"
        
    def _create_zip_archive(self, md_file_path: str, media_folder_path: str) -> str:
        """
        Create a ZIP archive with the Markdown file and media folder
        
        Args:
            md_file_path: Path to the Markdown file
            media_folder_path: Path to the media folder
            
        Returns:
            str: Path to the created ZIP archive
        """
        # Generate zip file path
        zip_path = os.path.splitext(md_file_path)[0] + ".zip"
        
        # Create zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add markdown file
            zipf.write(
                md_file_path, 
                os.path.basename(md_file_path)
            )
            
            # Add all files from media folder
            for root, _, files in os.walk(media_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate relative path for the file in the zip
                    rel_path = os.path.join(
                        os.path.basename(media_folder_path),
                        os.path.relpath(file_path, media_folder_path)
                    )
                    zipf.write(file_path, rel_path)
        
        return zip_path
    
    def _format_text_with_runs(self, paragraph: Paragraph) -> str:
        """
        Apply formatting to text runs
        
        Args:
            paragraph: A paragraph with formatted text runs
            
        Returns:
            str: Formatted text in Markdown
        """
        md_text = ""
        
        for run in paragraph.runs:
            text = run.get('text', '')
            if not text:
                continue
            
            # Get formatting flags
            is_bold = run.get('bold', False)
            is_italic = run.get('italic', False)
            is_underline = run.get('underline', False)
            is_strike = run.get('strike', False)
            
            # Check if we need to handle newlines in this run
            if '\n' in text and any([is_bold, is_italic, is_underline, is_strike]):
                # Split the text by newlines
                lines = text.split('\n')
                formatted_lines = []
                
                for i, line in enumerate(lines):
                    if not line and i < len(lines) - 1:
                        # Preserve empty lines that aren't at the end
                        formatted_lines.append('')
                        continue
                    
                    line_text = line
                    
                    # Only escape characters if no formatting is applied
                    # or text contains characters that need escaping
                    if any(c in line_text for c in '*_#`[]()'):
                        line_text = self._escape_markdown_chars(line_text)
                    
                    # Apply formatting to each line separately
                    if is_strike and line_text:
                        line_text = f"~~{line_text}~~"
                        
                    if is_underline and line_text:
                        line_text = f"<u>{line_text}</u>"
                        
                    if is_italic and line_text:
                        line_text = f"*{line_text}*"
                        
                    if is_bold and line_text:
                        line_text = f"**{line_text}**"
                    
                    formatted_lines.append(line_text)
                
                # Join the lines back with newlines
                md_text += '\n'.join(formatted_lines)
            else:
                # Process single-line text as before
                # Only escape characters if no formatting is applied
                # or text contains characters that need escaping
                if not any([is_bold, is_italic, is_underline, is_strike]) and any(c in text for c in '*_#`[]()'):
                    text = self._escape_markdown_chars(text)
                
                # Apply formatting (wrapping in reverse order of application)
                if is_strike:
                    text = f"~~{text}~~"
                    
                if is_underline:
                    text = f"<u>{text}</u>"
                    
                if is_italic:
                    text = f"*{text}*"
                    
                if is_bold:
                    text = f"**{text}**"
                    
                md_text += text
        
        return md_text
    
    def _escape_markdown_chars(self, text: str) -> str:
        """
        Escape special Markdown characters in text
        
        Args:
            text: Raw text
            
        Returns:
            str: Text with escaped Markdown characters
        """
        # This is a simplified approach that only escapes the most common
        # Markdown syntax characters that would affect formatting
        
        # First escape backslashes to prevent double-escaping
        text = text.replace('\\', '\\\\')
        
        # Escape characters that commonly have special meaning in Markdown
        replacements = [
            ('*', '\\*'),
            ('_', '\\_'),
            ('#', '\\#'),
            ('`', '\\`'),
            ('[', '\\['),
            (']', '\\]'),
            ('(', '\\('),
            (')', '\\)'),
        ]
        
        for old, new in replacements:
            text = text.replace(old, new)
                
        return text
    
    def _generate_markdown(self) -> str:
        """
        Generate Markdown content from the document model
        
        Returns:
            str: Complete Markdown content
        """
        md_content = ""
        
        # Reset current heading level
        self.current_heading_level = 0
        
        # Process all paragraphs
        for paragraph in self.document.paragraphs:
            md_content += self._format_paragraph(paragraph)
        
        return md_content
    
    def _save_images(self) -> None:
        """
        Save all images from the document to the media folder
        """
        # Get all images from the document
        images = self.document.get_images()
        
        # Save each image
        for image in images:
            image.save(self.media_folder) 