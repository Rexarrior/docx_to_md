from typing import Optional, Union, BinaryIO

class Image:
    """
    Container for image data and metadata.
    Represents an image extracted from the document.
    """
    
    def __init__(self):
        self.file_path: str = ""        # Original path in the docx
        self.content: bytes = None      # Binary content of the image
        self.new_file_name: str = ""    # Generated filename for the output
        self.alt_text: str = ""         # Alternative text for the image
        self.width: int = 0             # Width of the image
        self.height: int = 0            # Height of the image
        self.image_format: str = ""     # Format of the image (png, jpg, etc.)
        
    def save(self, output_dir: str) -> str:
        """
        Save the image to the specified directory
        
        Args:
            output_dir: Directory to save the image in
            
        Returns:
            str: Path to the saved image
        """
        pass 