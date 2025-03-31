# Python Script for Generating Markdown Files  

 **Markdown File Creation**  
   - Generate a `.md` file with the same name as the Word file.  
   - For each section and its heading level (with nested content), create the corresponding hierarchy using `- ` and **Tabs**:  
     - **Heading Level 1**: No tab  
     - **Heading Level 2**: 1 tab  
     - **Heading Level 3**: 2 tabs  
     - *(and so on...)*  

   - **Content under a heading** should be indented with **+1 tab** to indicate nesting.  

### Notes on Headings:  
1. Word headings may or may not have predefined styles.  

   

3. **Spacing Rules**:  
   - Add **2 line breaks** after headings.  
   - Add **2 line breaks** wherever there are empty lines in the Word document.  

4. **Special Characters**:  
   - Escape hyphens (`-`) not at the start of a line with a backslash: `\-`.  

5. **Text Formatting**:  
   Preserve Word formatting in Markdown:  
   - *Italic* → `*italic*`  
   - **Bold** → `**bold**`  
   - ***Bold Italic*** → `***bold italic***`  
   - <u>Underlined</u> → `__underlined__`  
   - ~~Strikethrough~~ → `~~strikethrough~~`  


6. **Lists**:  
   - Preserve **numbered** and **bulleted** lists.  


7. **Images**:  
   - Replace with the following syntax:  
     ```markdown
     ![image1.png](Markdown_filename/image1.jpg)
     ```  
   - Number images sequentially (e.g., `image1.jpg`, `image2.jpg`).  
   - Images MUST be in the same place in md file, as in docx file

8. **Tables**:  
   - Should be rewriten as an md table. MUST be in the same places in result md, as in the docx  
   

## Archive Creation  
1. Create a `.zip` archive containing:  
   - The `.md` file.  
   - A **content folder** (named after the `.md` file).  
     - The folder should include:  
       - Extracted images.  
       - Table screenshots.  
