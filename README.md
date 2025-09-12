# RST to Markdown Conversion Project Plan

## Overview
This document outlines the process for converting all RST documentation files to Markdown format using our custom converter. The plan focuses on a systematic approach to ensure all RST features are properly handled and the resulting Markdown files maintain the same quality and functionality as the original documentation.

## Phase 1: Analysis and Inventory (1-2 days)

### 1.1 Scan All RST Files Using rst_analyzer
- Create a script that uses our `rst_analyzer.py` to scan all RST files in the documentation directory
- Generate a comprehensive report of all RST features used across the documentation
- Identify frequency and distribution of different RST elements

```python
#!/usr/bin/env python3
import os
import sys
import argparse
from collections import Counter
from rst_analyzer import RSTAnalyzer

def analyze_directory(input_dir, output_file=None):
    """Analyze all RST files in a directory and generate a report."""
    analyzer = RSTAnalyzer()
    directives = Counter()
    roles = Counter()
    special_blocks = Counter()
    file_count = 0
    
    print(f"Scanning directory: {input_dir}")
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.rst'):
                file_path = os.path.join(root, file)
                print(f"Analyzing {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analyze the content
                file_directives, file_roles, file_blocks = analyzer.analyze(content)
                
                # Update counters
                directives.update(file_directives)
                roles.update(file_roles)
                special_blocks.update(file_blocks)
                file_count += 1
    
    # Generate report
    report = "RST Analysis Report\n"
    report += "=================\n\n"
    report += f"Total files analyzed: {file_count}\n\n"
    
    report += "Directives Used:\n"
    for directive, count in directives.most_common():
        report += f"  - {directive}: {count}\n"
    
    report += "\nRoles Used:\n"
    for role, count in roles.most_common():
        report += f"  - {role}: {count}\n"
    
    report += "\nSpecial Blocks:\n"
    for block, count in special_blocks.most_common():
        report += f"  - {block}: {count}\n"
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to {output_file}")
    else:
        print(report)
    
    return directives, roles, special_blocks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze RST files in a directory')
    parser.add_argument('input_dir', help='Input directory containing RST files')
    parser.add_argument('--output', help='Output file for the report')
    
    args = parser.parse_args()
    analyze_directory(args.input_dir, args.output)
```

### 1.2 Inventory Required Handlers
- Create a spreadsheet or document listing all RST features found in the analysis
- Compare against our current converter implementation to identify missing handlers
- Prioritize handlers based on frequency and complexity
- Document any special cases or edge cases that need custom handling

**Example Inventory Table:**

| RST Feature | Frequency | Current Handler | Status | Priority | Notes |
|-------------|-----------|----------------|--------|----------|-------|
| admonition  | 127       | Yes            | Complete | - | - |
| image       | 98        | Yes            | Complete | - | - |
| code-block  | 76        | Yes            | Complete | - | - |
| raw         | 45        | Yes            | Needs improvement | High | Issues with pre tags |
| table       | 32        | No             | Not implemented | High | - |
| toctree     | 28        | No             | Not implemented | Medium | - |
| include     | 15        | No             | Not implemented | Medium | - |
| math        | 8         | No             | Not implemented | Low | - |

## Phase 2: Converter Enhancement (2-3 days)

### 2.1 Implement Missing Handlers
- Add handlers for all missing RST features identified in the inventory
- Prioritize based on frequency and importance
- Follow the existing pattern of modular handler methods

### 2.2 Improve Existing Handlers
- Enhance handlers that need improvement based on the inventory
- Focus on edge cases and special formatting requirements
- Ensure consistent output across different contexts (e.g., blockquotes, lists)

### 2.3 Add Validation and Error Handling
- Implement validation for converted output
- Add robust error handling to prevent crashes on malformed RST
- Create detailed logging for troubleshooting

## Phase 3: Testing and Validation (2-3 days)

### 3.1 Unit Testing
- Create unit tests for each handler method
- Test with various input patterns and edge cases
- Ensure consistent output across different contexts

### 3.2 Sample File Testing
- Select representative RST files from each category/complexity level
- Convert and manually review the output
- Document any issues or inconsistencies

### 3.3 Automated Validation
- Create validation scripts to check for common issues:
  - Unclosed code blocks
  - Broken links
  - Missing images
  - Malformed tables
- Generate validation reports for each file

## Phase 4: Batch Processing Implementation (1-2 days)

### 4.1 Create Batch Processing Script
- Implement a script to process all RST files in a directory
- Add command-line options for input/output directories
- Include logging and error reporting

```python
#!/usr/bin/env python3
import os
import sys
import argparse
import logging
from rst_to_md_converter_updated import RSTToMarkdownConverter

def process_directory(input_dir, output_dir, backup_dir=None):
    """Process all RST files in a directory."""
    converter = RSTToMarkdownConverter()
    success_count = 0
    error_count = 0
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.rst'):
                rst_path = os.path.join(root, file)
                # Create equivalent path in output directory
                rel_path = os.path.relpath(rst_path, input_dir)
                md_path = os.path.join(output_dir, rel_path.replace('.rst', '.md'))
                
                # Create output directory if it doesn't exist
                os.makedirs(os.path.dirname(md_path), exist_ok=True)
                
                # Convert the file
                logging.info(f"Converting {rst_path} to {md_path}")
                try:
                    converter.convert_file(rst_path, md_path)
                    logging.info(f"Successfully converted {rst_path}")
                    success_count += 1
                except Exception as e:
                    logging.error(f"Error converting {rst_path}: {str(e)}")
                    error_count += 1
    
    logging.info(f"Conversion complete. Success: {success_count}, Errors: {error_count}")
    return success_count, error_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert RST files to Markdown')
    parser.add_argument('input_dir', help='Input directory containing RST files')
    parser.add_argument('output_dir', help='Output directory for Markdown files')
    parser.add_argument('--backup', help='Backup directory for original RST files')
    parser.add_argument('--log', help='Log file path', default='conversion.log')
    
    args = parser.parse_args()
    
    logging.basicConfig(
        filename=args.log,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    process_directory(args.input_dir, args.output_dir, args.backup)
```

### 4.2 Post-Processing
- Implement post-processing scripts for common fixes
- Update internal links to point to .md files instead of .rst
- Fix any image path issues

## Phase 5: Full Conversion and Quality Control (2-3 days)

### 5.1 Full Batch Conversion
- Run the batch processor on all RST files
- Monitor logs for errors
- Generate summary report of conversion results

### 5.2 Quality Control
- Perform automated validation on all converted files
- Sample manual review of representative files
- Document any issues for further improvement

### 5.3 Documentation Updates
- Update any references to RST files in documentation
- Update build scripts to work with Markdown
- Create documentation for maintaining Markdown files

## Timeline and Resources

### Timeline
- **Phase 1 (Analysis)**: 1-2 days
- **Phase 2 (Enhancement)**: 2-3 days
- **Phase 3 (Testing)**: 2-3 days
- **Phase 4 (Batch Processing)**: 1-2 days
- **Phase 5 (Full Conversion)**: 2-3 days
- **Total**: 8-13 days

### Resources Required
- Developer time: 1 person full-time
- Review time: 1-2 people part-time for quality control
- Storage space for both RST and MD versions during transition

## Success Criteria
- All RST files successfully converted to Markdown
- Markdown files render correctly in the documentation system
- All links, images, and special formatting preserved
- No regression in documentation quality or usability

## Maintenance Plan
- Document any remaining edge cases or issues
- Create guidelines for future Markdown documentation
- Set up periodic validation checks for documentation consistency
