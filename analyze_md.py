import os
import re

def analyze_markdown(file_path):
    """Analyze the structure of a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Markdown File: {os.path.basename(file_path)}")
    print(f"File size: {len(content)} characters")
    
    # Count lines
    lines = content.split('\n')
    print(f"Total lines: {len(lines)}")
    
    # Count headings
    headings = []
    for line in lines:
        if line.strip().startswith('#'):
            level = len(re.match(r'^#+', line).group())
            headings.append((level, line.strip()))
    
    print(f"\nHeadings: {len(headings)}")
    for level, heading in headings[:10]:  # First 10 headings
        print(f"  {'#' * level} {heading[level+1:].strip()}")
    
    # Count images
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    images = re.findall(image_pattern, content)
    print(f"\nImages: {len(images)}")
    for i, (alt, src) in enumerate(images[:5]):  # First 5 images
        print(f"  Image {i+1}: Alt: {alt} - Source: {src}")
    
    # Count tables
    table_rows = 0
    in_table = False
    for line in lines:
        if '|' in line and '-|-' in line.replace(' ', ''):
            in_table = True
        elif in_table and '|' in line:
            table_rows += 1
        elif in_table and not ('|' in line):
            in_table = False
    
    print(f"\nEstimated table rows: {table_rows}")
    
    # Check formatting
    bold_count = len(re.findall(r'\*\*[^*]+\*\*', content))
    italic_count = len(re.findall(r'\*[^*]+\*', content))
    
    print(f"\nFormatting:")
    print(f"  Bold: {bold_count} occurrences")
    print(f"  Italic: {italic_count} occurrences")
    
    # Line breaks after headings
    heading_followed_by_empty = 0
    for i in range(len(lines) - 1):
        if lines[i].strip().startswith('#') and not lines[i+1].strip():
            heading_followed_by_empty += 1
    
    print(f"\nStructure:")
    print(f"  Headings followed by empty line: {heading_followed_by_empty}")
    
    # Sample content
    print("\nSample content (first 10 non-empty lines):")
    count = 0
    for line in lines:
        if line.strip():
            print(f"  {line[:50]}...")
            count += 1
            if count >= 10:
                break

if __name__ == "__main__":
    analyze_markdown("result_example/document.md") 