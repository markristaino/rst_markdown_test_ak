from docutils.core import publish_doctree
from docutils import nodes
import json
import re
from collections import Counter

class SimpleRSTAnalyzer:
    def __init__(self):
        self.stats = {
            'directives': Counter(),
            'roles': Counter(),
            'admonitions': Counter(),
            'raw_html': 0,
            'sections': [],
            'custom_elements': []
        }
        # Regex patterns to find directives in the source
        self.directive_pattern = re.compile(r'\.\. +([a-zA-Z0-9_-]+)::', re.MULTILINE)
        self.raw_html_pattern = re.compile(r'\.\. +raw:: +html', re.MULTILINE)
        self.admonition_pattern = re.compile(r'\.\. +(note|warning|admonition|attention|caution|danger|error|hint|important|tip)::', re.MULTILINE)
        
    def analyze_file(self, rst_file):
        """Analyze a single RST file and extract its structure."""
        try:
            with open(rst_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use regex to find directives in the source
            directives = self.directive_pattern.findall(content)
            for directive in directives:
                self.stats['directives'][directive] += 1
                
            # Find raw HTML blocks
            raw_html_blocks = self.raw_html_pattern.findall(content)
            self.stats['raw_html'] = len(raw_html_blocks)
            
            # Find admonitions
            admonitions = self.admonition_pattern.findall(content)
            for admonition in admonitions:
                self.stats['admonitions'][admonition] += 1
            
            # Parse the RST into a document tree for more detailed analysis
            doctree = publish_doctree(content)
            
            # Process the document tree
            self._process_node(doctree)
            
            return self.stats
            
        except Exception as e:
            print(f"Error processing {rst_file}: {e}")
            return None
    
    def _process_node(self, node):
        """Process a node in the document tree."""
        # Check for roles
        if hasattr(node, 'tagname') and node.tagname == 'title_reference':
            self.stats['roles']['title_reference'] += 1
            
        # Check for sections
        if isinstance(node, nodes.section):
            title = ''
            for child in node.children:
                if isinstance(child, nodes.title):
                    title = child.astext()
                    break
            self.stats['sections'].append({
                'title': title,
                'level': len(node.get('ids', []))
            })
            
        # Check for custom elements or extensions
        if hasattr(node, 'tagname') and node.tagname not in ('document', 'section', 'paragraph', 'text'):
            if node.tagname not in ('title', 'reference', 'target', 'literal', 'emphasis', 'strong', 'title_reference'):
                if node.tagname not in self.stats['custom_elements']:
                    self.stats['custom_elements'].append(node.tagname)
                
        # Process children recursively
        if hasattr(node, 'children'):
            for child in node.children:
                self._process_node(child)
    
    def generate_report(self):
        """Generate a detailed report of RST usage patterns."""
        report = {
            'summary': {
                'total_directives': sum(self.stats['directives'].values()),
                'unique_directives': len(self.stats['directives']),
                'total_raw_html': self.stats['raw_html'],
                'total_admonitions': sum(self.stats['admonitions'].values()),
                'total_sections': len(self.stats['sections'])
            },
            'directives': dict(self.stats['directives']),
            'roles': dict(self.stats['roles']),
            'admonitions': dict(self.stats['admonitions']),
            'sections': self.stats['sections'],
            'custom_elements': self.stats['custom_elements']
        }
        
        return report

if __name__ == "__main__":
    analyzer = SimpleRSTAnalyzer()
    stats = analyzer.analyze_file('integrations.rst')
    report = analyzer.generate_report()
    print(json.dumps(report, indent=2))
