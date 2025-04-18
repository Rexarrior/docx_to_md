# Active Context

## Current Focus
We've recently fixed the handling of newlines within paragraphs in the Markdown output. The issue was related to maintaining proper indentation for lines that were split by newlines within the same paragraph and ensuring that formatting (bold, italic, etc.) is correctly applied to each line individually. We implemented a solution that preserves the document's hierarchical structure and ensures consistent indentation and formatting throughout multi-line paragraphs.

## Recent Developments
- Implemented Document, Paragraph, Image, and Table model classes
- Created and tested the DocxParser with TDD approach
- Successfully parsed the example document
- Fixed table detection issue to preserve document flow
- Created special test scripts to verify table positioning
- Implemented the MarkdownWriter with full functionality
- Created test scripts to verify the conversion pipeline
- Enhanced heading level detection to properly recognize different heading levels
- Created a test script to verify proper heading level conversion
- Fixed newline handling in paragraphs to maintain proper indentation throughout
- Enhanced the _format_text_with_runs method to handle newlines in formatted text correctly
- Created a test script (test_newlines.py) to verify newline handling
- All tests pass with the updated implementation

## Parser Implementation Insights
- Heading detection now examines multiple factors:
  - Official "Heading" style names with numeric level indicators
  - Other style names like "Title" and "Subtitle"
  - Font sizes of paragraph text
  - Bold formatting with additional heuristics (ALL CAPS text, text length)
- Tables are correctly parsed with rows and columns preserved in proper document flow
- Images are extracted with their binary content
- Text formatting information (bold, italic, etc.) is preserved in runs
- Document structure hierarchy is maintained
- Direct access to document body elements preserves exact ordering

## MarkdownWriter Implementation Insights
- Text formatting is properly converted to Markdown syntax (bold to **bold**, italic to *italic*, etc.)
- Images are extracted and saved in a media folder, with correct path references in Markdown
- Tables are converted to Markdown using pipe syntax with proper alignment
- Heading levels are properly translated to corresponding Markdown heading syntax (# for level 1, ## for level 2, etc.)
- Document structure is preserved with headings, paragraphs, and other elements
- Special characters are escaped in Markdown to prevent formatting issues
- ZIP archives are created with proper structure, containing the Markdown file and media folder
- Paragraphs with newlines maintain proper indentation throughout with tabs based on heading level
- Formatted text runs with newlines have formatting (bold, italic, etc.) correctly applied to each line separately

## Current Priorities
1. Implement error handling for edge cases
2. Enhance the command-line interface
3. Add more comprehensive testing
4. Complete documentation

## Active Decisions
- **Parser Implementation**: Using python-docx to extract content from DOCX files
- **Document Flow**: Processing paragraphs and tables in order by directly accessing document body elements
- **Heading Detection**: Using a multi-faceted approach that considers styles, font sizes, bold formatting, and text properties
- **Font Size Analysis**: Added helper method to extract font sizes from paragraph runs, supporting heading level determination
- **Image Processing**: Extracting and sequentially numbering images
- **Table Processing**: Converting tables to Markdown tables with proper alignment
- **Test-Driven Development**: Using pytest for unit testing the parser
- **Text Formatting**: Converting bold to `**bold**`, italic to `*italic*`, etc.
- **Heading Conversion**: Translating heading levels to corresponding Markdown headings with the appropriate number of # symbols
- **Image Handling**: Saving images in a media folder and referencing them with proper paths
- **Table Formatting**: Converting tables to Markdown using pipe syntax with proper alignments
- **ZIP Structure**: Organizing the output as a Markdown file and a media folder in a ZIP archive
- **Newline Handling**: Ensuring that lines split by newlines within the same paragraph maintain proper indentation
- **Formatted Text with Newlines**: Applying formatting markers to each line individually when text contains newlines

## Next Steps
1. Implement error handling for edge cases (file access issues, malformed documents, etc.)
2. Enhance the command-line interface with better user feedback and options
3. Add more comprehensive testing for different document types and edge cases
4. Complete documentation including usage examples and API reference

## Current Conversion Process Insights
- **Document Flow**: Elements are processed in the exact order they appear in the source document
- **Text Formatting**: Bold text in Word is converted to `**bold**` in Markdown
- **Heading Structure**: Heading levels are detected from styles, font sizes, and formatting attributes
- **Image Handling**: Images from the docx are extracted and referenced in Markdown with the format `![alt_text](image_name.png)`
- **Image Naming**: Images are named sequentially (document.002.png, document.003.png, etc.)
- **Table Conversion**: Tables are converted to Markdown table syntax with proper alignment indicators (`:-)`)
- **Whitespace**: Double line breaks are used after headings and empty paragraphs
- **Image Path Handling**: Images are saved in a media folder and referenced in Markdown using relative paths
- **Document Hierarchy**: All document elements are processed in the order they appear in the source
- **Escape Handling**: Special Markdown characters are escaped to prevent formatting issues
- **Archive Creation**: ZIP archives are created with proper structure for easy distribution
- **Paragraph Indentation**: Indentation is maintained throughout paragraphs with newlines based on heading level
- **Formatting Continuity**: Formatting is applied to each line individually when text contains newlines

## Heading Level Detection Enhancement
- Enhanced the `_detect_heading_level` method to use multiple approaches for determining heading levels:
  - First checking for official heading styles (Heading 1, Heading 2, etc.)
  - Looking for other style names like "Title" and "Subtitle"
  - Analyzing font sizes with graduated thresholds for different heading levels
  - Considering text characteristics like case (ALL CAPS) and length
- Added a new helper method `_get_font_size` to extract and normalize font size information
- Created a specialized test script (`test_heading_levels.py`) to verify heading level detection
- Test results confirmed proper heading level distribution in the output markdown

## Newline Handling Enhancement
- Enhanced the `_add_indent_after_newlines` method to ensure proper indentation after each newline in paragraph text
- Modified the `_format_text_with_runs` method to handle newlines in formatted text properly:
  - Text is split by newlines and each line is formatted individually
  - Formatting markers (bold, italic, etc.) are applied to each line separately
  - Empty lines within text are preserved (except at the end)
  - Markdown characters are escaped properly if needed
- Created a specialized test script (`test_newlines.py`) to verify newline handling:
  - Tests various paragraph types with newlines (plain text, formatted text, bullet lists)
  - Verifies that indentation is maintained throughout paragraphs
  - Confirms that formatting is correctly applied to each line
- Test results confirmed proper newline handling in the output markdown

## Open Questions
- Best approach for handling complex nested lists
- Strategy for handling different text formatting combinations
- Approach for managing large documents efficiently
- How to handle uncommon Word features without Markdown equivalents 