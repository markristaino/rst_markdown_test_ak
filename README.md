# RST to Markdown Conversion Project Plan

## Overview
This document outlines the process for converting all RST documentation files to Markdown format using our custom converter, [rst_to_md_converter_updated.py](https://github.com/markristaino/rst_markdown_test_ak/blob/main/rst_to_md_converter_updated.py). The plan focuses on a systematic approach to ensure all RST features are properly handled and the resulting Markdown files maintain the same or good-enough quality and functionality as the original documentation.

Mark has already done a "proof-of-concept" run, by writing a script that coverted https://docs.actionkit.com/docs/manual/integrations.html into [readable and well-formatted markdown.](https://docsify-this.net/?basePath=https://raw.githubusercontent.com/markristaino/rst_markdown_test_ak/main&homepage=integrations.md#/). During his proof-of-concept, he identified and built 11 handlers that are displayed in the below table.

## Phase 1: Analysis and Inventory (1-2 days)

### 1.1 Inventory And Scan All RST Files Using rst_analyzer
- Create a script that uses our [rst_analyzer.py](https://github.com/markristaino/rst_markdown_test_ak/blob/main/) to inventory and scan all RST files in the AK docs directory
- Generate a comprehensive report of all RST features used across the documentation
- Identify frequency and distribution of different RST elements


### 1.2 Inventory Required Handlers
- Update the below spreadsheet and listing all RST features found in the analysis
- Compare against our current converter implementation to identify missing handlers
- Prioritize handlers based on frequency and complexity
- Document any special cases or edge cases that need custom handling

**RST Feature Inventory Table:**

| RST Feature | Current Handler | Status | Priority | Notes |
|-------------|----------------|--------|----------|-------|
| section headers | Yes | Complete | - | Handles all heading levels |
| admonition  | Yes | Complete | - | Converts to Markdown blockquotes with styling |
| note        | Yes | Complete | - | Converts to styled blockquotes |
| warning     | Yes | Complete | - | Converts to styled blockquotes |
| raw html    | Yes | Complete | - | Handles pre tags and style blocks |
| links       | Yes | Complete | - | Converts RST links to Markdown format |
| images      | Yes | Complete | - | Preserves attributes using HTML when needed |
| code-block  | Yes | Complete | - | Converts to Markdown code blocks with language |
| inline code | Yes | Complete | - | Converts to Markdown backticks |
| lists       | Yes | Complete | - | Handles both ordered and unordered lists |
| blockquotes | Yes | Complete | - | Properly formats nested content |
| tables      | No  | Not implemented | High | Need to handle simple and complex tables |
| toctree     | No  | Not implemented | Medium | Table of contents directive |
| include     | No  | Not implemented | Medium | File inclusion directive |
| math        | No  | Not implemented | Low | Mathematical equations |
| footnotes   | No  | Not implemented | Low | Reference notes |
| substitutions | No | Not implemented | Low | Text replacement feature |
| glossary    | No  | Not implemented | Low | Term definitions |
| index       | No  | Not implemented | Low | Index entries |
| literalinclude | No | Not implemented | Medium | Code inclusion from external files |
## Phase 2: Converter Enhancement (2-3 days)

### 2.1 Implement Missing Handlers
- Add handlers for all missing RST features identified in the inventory to the file  `rst_to_md_converter_updated.py` 
- Prioritize based on frequency and importance
- Follow the existing pattern of modular handler methods

### 2.2 Improve Existing Handlers
- Enhance handlers that need improvement based on the inventory
- Focus on edge cases and special formatting requirements
- Ensure consistent output across different contexts (e.g., blockquotes, lists)

### 2.3 Add Validation and Error Handling
- Create validation scripts to check for common issues:
  - Unclosed code blocks
  - Broken links
  - Missing images
  - Malformed tables

## Phase 3: Testing and Validation (2-3 days)

### 3.1 Sample File Testing
- Select representative RST files from each category/complexity level
- Convert and manually review the output
- Document any issues or inconsistencies in the **RST Feature Inventory Table:**
- Generate validation reports for each file


## Phase 4: Batch Processing Implementation (1-2 days)

### 4.1 Create Batch Processing Script
- Implement a script to process all RST files in a directory
- Add command-line options for input/output directories
- Include logging and error reporting

### 4.2 Post-Processing
- Implement post-processing scripts for common fixes
- Update internal links to point to correct URLs

