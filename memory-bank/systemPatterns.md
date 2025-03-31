# System Patterns

## Architecture Overview
The Word-to-Markdown converter follows a pipeline architecture with several processing stages:

```
[Input .docx File] → [Document Parser] → [Content Extractor] → [Markdown Generator] → [Media Handler] → [Archive Creator] → [Output .md + ZIP]
```

## Component Relationships
1. **Document Parser**: Reads and parses the Word document structure, detecting heading levels, formatting, and other elements
2. **Content Extractor**: Extracts text, formatting, images, and tables
3. **Markdown Generator**: Converts extracted content to Markdown format with proper heading hierarchies
4. **Media Handler**: Processes and saves images and other media
5. **Archive Creator**: Packages the Markdown file and media folder into a ZIP archive

## Design Patterns
- **Pipeline Pattern**: For sequential processing of the document
- **Strategy Pattern**: For handling different content types (text, images, tables)
- **Factory Pattern**: For creating appropriate content handlers based on element type
- **Visitor Pattern**: For traversing the document structure while maintaining separation of concerns
- **Composite Pattern**: For representing hierarchical document structure with proper heading levels

## Hierarchical Heading Detection
The system uses a multi-faceted approach to detect heading levels:
1. **Style-based Detection**: Checks for standard heading styles like "Heading 1", "Heading 2"
2. **Named Style Detection**: Recognizes common heading style names like "Title", "Subtitle"
3. **Font Size Analysis**: Uses font size thresholds to determine heading importance
4. **Formatting Analysis**: Considers text properties like bold, ALL CAPS, and length

## Data Flow
1. Load .docx file into memory
2. Extract document structure and content with proper hierarchies
3. Process each element according to its type
4. Determine heading levels using multi-faceted detection
5. Generate properly formatted Markdown with appropriate heading markers
6. Extract and save media files
7. Create output directory structure
8. Package everything into a ZIP archive

## Error Handling Strategy
- Graceful degradation for unsupported elements
- Detailed logging for conversion errors
- Fallback mechanisms for complex formatting
- Validation steps to ensure output consistency 