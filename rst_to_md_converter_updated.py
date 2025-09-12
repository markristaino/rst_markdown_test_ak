#!/usr/bin/env python3
"""
RST to Markdown converter for ActionKit documentation.
This script converts RST files to Markdown, handling special cases like admonitions,
raw HTML blocks, and custom directives.
"""

import re
import os
import sys
from docutils.core import publish_doctree
from docutils import nodes

class RSTToMarkdownConverter:
    def __init__(self):
        # Regex patterns for RST elements
        self.section_pattern = re.compile(r'^([=~\-`\'":^_*+#])\1{2,}\s*$', re.MULTILINE)
        self.directive_pattern = re.compile(r'\.\.\s+([a-zA-Z0-9_-]+)::(.*?)(?=\n\S|\n\n\n|\n\.\.|$)', re.DOTALL)
        self.link_pattern = re.compile(r'`([^`]+)\s+<([^>]+)>`_')
        self.image_pattern = re.compile(r'\.\.\s+image::\s+(.*?)(?=\n\S|\n\n|\n\.\.|$)', re.DOTALL)
        
    def convert_file(self, rst_file, md_file=None):
        """Convert an RST file to Markdown."""
        if md_file is None:
            md_file = os.path.splitext(rst_file)[0] + '.md'
            
        with open(rst_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Convert the content
        md_content = self.convert_content(content)
        
        # Write the converted content
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        return md_file
    
    def convert_content(self, content):
        """Convert RST content to Markdown."""
        # Process the content in stages
        
        # 1. Handle section headers
        content = self.convert_section_headers(content)
        
        # 2. Handle admonitions and notes
        content = self.convert_admonitions(content)
        
        # 3. Handle raw HTML blocks
        content = self.convert_raw_html(content)
        
        # 4. Handle links
        content = self.convert_links(content)
        
        # 5. Handle images
        content = self.convert_images(content)
        
        # 5b. Handle inline image attributes
        content = self.convert_inline_image_attributes(content)
        
        # 6. Handle code blocks
        content = self.convert_code_blocks(content)
        
        # 7. Clean up any remaining RST-specific syntax
        content = self.clean_up(content)
        
        return content
    
    def convert_section_headers(self, content):
        """Convert RST section headers to Markdown headers."""
        lines = content.split('\n')
        result = []
        
        i = 0
        while i < len(lines):
            # Check if the current line is a potential header
            if i + 1 < len(lines) and self.section_pattern.match(lines[i + 1]):
                # This is a header, determine the level
                underline_char = lines[i + 1][0]
                level = self._get_header_level(underline_char)
                
                # Add the header with appropriate markdown syntax
                result.append(f"{'#' * level} {lines[i]}")
                i += 2  # Skip the underline
            else:
                result.append(lines[i])
                i += 1
                
        return '\n'.join(result)
    
    def _get_header_level(self, char):
        """Determine header level based on the underline character."""
        # Common RST header hierarchy
        if char == '=':
            return 1
        elif char == '-':
            return 2
        elif char == '~':
            return 2  # Sometimes used as second level
        elif char == '^':
            return 3
        elif char == '"':
            return 4
        else:
            return 3  # Default for other characters
    
    def convert_admonitions(self, content):
        """Convert RST admonitions to Markdown blockquotes."""
        def replace_admonition(match):
            directive = match.group(1)
            admonition_content = match.group(2).strip()
            
            # Pre-process any raw HTML blocks within the admonition
            raw_html_pattern = r'\.\.\s+raw::\s+html\s*\n\n(.*?)(?=\n\S|\n\n\n|\n\.\.|$)'
            
            def process_raw_html(html_match):
                html_content = html_match.group(1).strip()
                
                # Check if this is a <pre> block that should be preserved as code
                if re.match(r'^\s*<pre>', html_content):
                    # For <pre> blocks in admonitions, extract the content without code block markers
                    pre_content = re.sub(r'^\s*<pre>(.*?)</pre>\s*$', r'\1', html_content, flags=re.DOTALL)
                    return pre_content.strip()
                elif re.match(r'^\s*<style>', html_content):
                    # For style blocks, preserve them as actual HTML
                    return html_content
                else:
                    # For other HTML, include directly
                    return html_content
            
            # Process any raw HTML in the content
            admonition_content = re.sub(raw_html_pattern, process_raw_html, admonition_content, flags=re.DOTALL)
            
            # Format based on directive type
            if directive.lower() == 'note':
                return f"> **Note**\n> \n{self._format_blockquote_content(admonition_content)}"
            elif directive.lower() == 'warning':
                return f"> **Warning**\n> \n{self._format_blockquote_content(admonition_content)}"
            elif directive.lower() == 'admonition':
                # Extract the admonition title if present
                title_match = re.match(r'^\s*([^\n]+)', admonition_content)
                title = title_match.group(1) if title_match else "Info"
                content_without_title = admonition_content[len(title_match.group(0)):] if title_match else admonition_content
                
                return f"> **{title.strip()}**\n> \n{self._format_blockquote_content(content_without_title.strip())}"
            else:
                # Generic handling for other directives
                return f"> **{directive.capitalize()}**\n> \n{self._format_blockquote_content(admonition_content)}"
        
        # Find and replace all admonition directives
        pattern = r'\.\.\s+(note|warning|admonition|attention|caution|danger|error|hint|important|tip)::(.*?)(?=\n\S|\n\n\n|\n\.\.|$)'
        content = re.sub(pattern, replace_admonition, content, flags=re.DOTALL)
        
        return content
    
    def _format_blockquote_content(self, content):
        """Format content for use in a Markdown blockquote."""
        # Add '> ' prefix to each line
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():
                formatted_lines.append(f"> {line}")
            else:
                formatted_lines.append(">")
                
        return '\n'.join(formatted_lines)
    
    def convert_raw_html(self, content):
        """Handle raw HTML blocks in RST."""
        def replace_raw_html(match):
            html_content = match.group(1).strip()
            
            # Get context to determine if this is in an admonition/blockquote
            context_before = match.string[:match.start()].split('\n')[-5:]
            in_admonition = any(line.startswith('   ') for line in context_before)
            
            # Check if this is a <pre> block that should be preserved as code
            if re.match(r'^\s*<pre>', html_content):
                # For <pre> blocks, extract the content and use plain text
                pre_content = re.sub(r'^\s*<pre>(.*?)</pre>\s*$', r'\1', html_content, flags=re.DOTALL)
                # Remove any HTML tags from the pre content
                pre_content = pre_content.strip()
                
                if in_admonition:
                    # For pre blocks in admonitions, we need to handle them differently
                    # Just return the content directly without code block markers
                    return pre_content
                else:
                    # Regular pre block - use code block
                    return f"\n```\n{pre_content}\n```\n"
            elif re.match(r'^\s*<style>', html_content):
                # For style blocks, preserve them as actual HTML
                return f"\n\n{html_content}\n\n"
            else:
                # For other HTML, include directly
                return f"\n\n{html_content}\n\n"
        
        # Find and replace raw HTML directives
        pattern = r'\.\.\s+raw::\s+html\s*\n\n(.*?)(?=\n\S|\n\n\n|\n\.\.|$)'
        content = re.sub(pattern, replace_raw_html, content, flags=re.DOTALL)
        
        # Remove any 'html' text that appears in blockquotes
        content = re.sub(r'(>\s*)html\s*\n', r'\1\n', content)
        
        return content
    
    def convert_links(self, content):
        """Convert RST links to Markdown links."""
        # Convert RST link syntax: `text <url>`_ to Markdown: [text](url)
        content = re.sub(r'`([^`]+)\s+<([^>]+)>`_', r'[\1](\2)', content)
        
        return content
    
    def convert_images(self, content):
        """Convert RST image directives to Markdown image syntax."""
        def replace_image(match):
            image_content = match.group(1).strip()
            
            # Extract image path and attributes
            lines = image_content.split('\n')
            image_path = lines[0].strip()
            
            # Extract attributes if present
            alt_text = ""
            width = ""
            align = ""
            css_class = ""
            
            for line in lines[1:]:
                line = line.strip()
                if line.startswith(':alt:'):
                    alt_text = line[5:].strip()
                elif line.startswith(':width:'):
                    width = line[7:].strip()
                elif line.startswith(':align:'):
                    align = line[7:].strip()
                elif line.startswith(':class:'):
                    css_class = line[7:].strip()
            
            # Basic Markdown image
            md_image = f"![{alt_text}]({image_path})"
            
            # If we have width or alignment, we need to use HTML
            if width or align or css_class:
                align_style = f"text-align: {align};" if align else ""
                width_style = f"width: {width};" if width else ""
                style = f" style=\"{align_style}{width_style}\"" if align_style or width_style else ""
                class_attr = f" class=\"{css_class}\"" if css_class else ""
                
                md_image = f"<img src=\"{image_path}\" alt=\"{alt_text}\"{style}{class_attr}>"
                
                # If centered, wrap in div
                if align == "center":
                    md_image = f"<div style=\"text-align: center;\">{md_image}</div>"
            
            return md_image
        
        # Find and replace image directives
        pattern = r'\.\.\s+image::\s+(.*?)(?=\n\S|\n\n\n|\n\.\.|$)'
        content = re.sub(pattern, replace_image, content, flags=re.DOTALL)
        
        return content
    
    def convert_inline_image_attributes(self, content):
        """Convert inline image attributes that appear after an image."""
        # Find lines that look like image attributes after an image
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            # Check if this line is an image in Markdown format, with or without blockquote prefix
            img_match = re.match(r'^(>\s*)?\!\[(.*?)\]\((.*?)\)\s*$', line)
            
            if img_match and i + 1 < len(lines) and re.match(r'^(>\s*)?\s*:[a-zA-Z]+:', lines[i+1]):
                # We found an image followed by attribute lines
                prefix = img_match.group(1) or ''
                alt_text = img_match.group(2)
                image_path = img_match.group(3)
                
                # Collect all attribute lines
                attr_lines = []
                j = i + 1
                while j < len(lines) and re.match(r'^(>\s*)?\s*:[a-zA-Z]+:', lines[j]):
                    # Strip the blockquote prefix if present
                    attr_line = lines[j]
                    attr_match = re.match(r'^(>\s*)?(.*?)$', attr_line)
                    if attr_match:
                        attr_lines.append(attr_match.group(2).strip())
                    j += 1
                
                # Extract attributes
                width = ""
                align = ""
                css_class = ""
                for attr in attr_lines:
                    if attr.startswith(':alt:'):
                        alt_text = attr[5:].strip()
                    elif attr.startswith(':width:'):
                        width = attr[7:].strip()
                    elif attr.startswith(':align:'):
                        align = attr[7:].strip()
                    elif attr.startswith(':class:'):
                        css_class = attr[7:].strip()
                
                # Create HTML image with attributes
                align_style = f"text-align: {align};" if align else ""
                width_style = f"width: {width};" if width else ""
                style = f" style=\"{align_style}{width_style}\"" if align_style or width_style else ""
                class_html = f" class=\"{css_class}\"" if css_class else ""
                
                html_image = f"<img src=\"{image_path}\" alt=\"{alt_text}\"{style}{class_html}>"
                
                # If centered, wrap in div
                if align == "center":
                    html_image = f"<div style=\"text-align: center;\">{html_image}</div>"
                
                # Add the converted image with the original prefix and skip the attribute lines
                result.append(f"{prefix}{html_image}")
                i = j
            else:
                # Just a regular line, add it as is
                result.append(line)
                i += 1
        
        return '\n'.join(result)
    
    def convert_code_blocks(self, content):
        """Convert RST code blocks to Markdown code blocks."""
        # Convert code blocks with double colon
        content = re.sub(r'::[ \t]*\n\n([ \t]+[^\n]+\n)+', self._format_code_block, content)
        
        # Convert literal blocks
        content = re.sub(r'\.\.\s+code::\s+([^\n]+)\n\n([ \t]+[^\n]+\n)+', self._format_code_block_with_language, content)
        
        return content
    
    def _format_code_block(self, match):
        """Format a code block for Markdown."""
        code = match.group(0)
        # Remove the double colon
        code = re.sub(r'::[ \t]*\n', '\n', code)
        # Remove the indentation
        code = re.sub(r'\n[ \t]+', '\n', code)
        # Add markdown code block syntax
        return f"\n```\n{code.strip()}\n```\n"
    
    def _format_code_block_with_language(self, match):
        """Format a code block with language specification for Markdown."""
        language = match.group(1).strip()
        code = match.group(2)
        # Remove the indentation
        code = re.sub(r'\n[ \t]+', '\n', code)
        # Add markdown code block syntax with language
        return f"\n```{language}\n{code.strip()}\n```\n"
    
    def clean_up(self, content):
        """Clean up any remaining RST-specific syntax."""
        # Remove any remaining RST directives
        content = re.sub(r'\.\.\s+[a-zA-Z0-9_-]+::', '', content)
        
        # Remove any remaining RST comments
        content = re.sub(r'\.\.\s+[^\n]*\n', '', content)
        
        # Remove any remaining image attributes
        content = re.sub(r'^\s*:[a-zA-Z]+:.*?$', '', content, flags=re.MULTILINE)
        
        # Remove any 'html' text that appears before code blocks
        content = re.sub(r'>\s*html\s*\n>\s*\n>\s*', '> \n> ', content)
        
        # Fix code blocks
        content = self._fix_code_blocks(content)
        
        # Fix multiple consecutive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content
        
    def _fix_code_blocks(self, content):
        """Fix issues with code blocks."""
        # First, handle the specific URL patterns we know about
        # These are exact patterns that need special handling
        
        # Pattern 1: First URL in ActBlue section
        pattern1 = r'(>\s*Select "ActBlue Default".*?endpoint URL follow this format:\s*\n>\s*\n>\s*)```\s*\n>\s*(https?://\[your actionkit hostname\]/webhooks/actblue/payments/\?account=Default%20ActBlue&backfill=1)\s*\n>\s*```'
        content = re.sub(pattern1, r'\1\2', content, flags=re.DOTALL)
        
        # Pattern 2: Second URL in ActBlue section
        pattern2 = r'(>\s*If you would like to backfill.*?backfill URL would be:\s*\n>\s*\n>\s*)```\s*\n>\s*(https?://\[your actionkit hostname\]/webhooks/actblue/payments/\?account=\[account info used for endpoint URL\]&backfill=1)\s*\n>\s*```'
        content = re.sub(pattern2, r'\1\2', content, flags=re.DOTALL)
        
        # Remove any 'html' text that appears in blockquotes
        content = re.sub(r'(>\s*)html\s*\n', r'\1\n', content)
        
        # Fix broken code blocks in blockquotes
        lines = content.split('\n')
        in_code_block = False
        in_blockquote = False
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Special case for URLs in code blocks within blockquotes
            if in_blockquote and i + 2 < len(lines):
                if line.strip() == '> ```' and lines[i+1].strip().startswith('> http'):
                    # Look for closing code block
                    j = i + 2
                    while j < len(lines) and not lines[j].strip() == '> ```':
                        j += 1
                    
                    if j < len(lines) and lines[j].strip() == '> ```':
                        # Found a URL in code blocks - remove the code blocks
                        result.append(lines[i+1])  # Add just the URL line
                        i = j + 1  # Skip past the closing code block
                        continue
            
            # Track if we're in a blockquote
            if line.startswith('>'):
                in_blockquote = True
            elif line.strip() == '' and i+1 < len(lines) and not lines[i+1].startswith('>'):
                in_blockquote = False
            
            # Track code blocks
            if '```' in line:
                in_code_block = not in_code_block
            
            # Fix pre tags in code blocks
            if in_code_block and '<pre>' in line:
                line = line.replace('<pre>', '')
            if in_code_block and '</pre>' in line:
                line = line.replace('</pre>', '')
            
            result.append(line)
            i += 1
        
        # Ensure all code blocks are closed
        content = '\n'.join(result)
        
        # Count backticks to see if we have unclosed code blocks
        backtick_count = content.count('```')
        if backtick_count % 2 == 1:
            content += '\n```'
        
        return content

if __name__ == "__main__":
    # Check if a file was specified
    if len(sys.argv) > 1:
        rst_file = sys.argv[1]
    else:
        rst_file = 'integrations.rst'  # Default to integrations.rst
    
    converter = RSTToMarkdownConverter()
    md_file = converter.convert_file(rst_file)
    
    print(f"Converted {rst_file} to {md_file}")
