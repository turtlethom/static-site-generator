import re

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_title(markdown: str):
    match = re.search(r'^#\s+(.*\S)\s*$', markdown, re.MULTILINE)
    if match:
        return match.group(1)
    raise ValueError("No h1 header found in markdown")
