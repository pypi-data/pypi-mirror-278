import re

class Markdown:
    def __init__(self, markdown_text):
        self.markdown_text = markdown_text
        self.headings = self._parse_headings()
        self.content_tree = self._generate_content_tree()

    def _parse_headings(self):
        headings = []
        content = []
        current_heading = None

        for line in self.markdown_text.splitlines():
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                if current_heading:
                    headings.append((current_heading[0], current_heading[1], "\n".join(content).strip()))
                level = len(match.group(1))
                title = match.group(2).strip()
                current_heading = (level, title)
                content = []
            else:
                content.append(line)
        
        if current_heading:
            headings.append((current_heading[0], current_heading[1], "\n".join(content).strip()))
        
        return headings

    def _generate_content_tree(self):
        tree = []
        stack = []

        for level, title, text in self.headings:
            while stack and stack[-1][0] >= level:
                stack.pop()
            
            node = {'title': title, 'text': text, 'children': []}
            if stack:
                stack[-1][1]['children'].append(node)
            else:
                tree.append(node)
            
            stack.append((level, node))
        
        return tree

    def _tree_to_string(self, tree, highlight_text=None):
        def node_to_string(node):
            if highlight_text and highlight_text in node['text']:
                result = f"**{node['title']}**"
            else:
                result = node['title']
            
            if node['children']:
                children = ', '.join(node_to_string(child) for child in node['children'])
                result += f' [{children}]'
            return result
        
        return ', '.join(node_to_string(node) for node in tree)

    def outline(self, text_to_highlight=None):
        return self._tree_to_string(self.content_tree, text_to_highlight)

def main():
    print("📝")