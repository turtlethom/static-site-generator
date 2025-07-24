from nodes.textnode import TextNode
from nodes.htmlnode import LeafNode, HTMLNode, ParentNode
from functions.splitters import split_node_delimiter, split_nodes_image, split_nodes_link
from enum_types import TextType, BlockType
import re

def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    if not text_type in TextType:
        raise Exception("Text node has invalid text type")
    match (text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            props = {"href": text_node.url}
            return LeafNode("a", text_node.text, props)
        case TextType.IMAGE:
            props = {
                "src": text_node.url,
                "alt": ""
            }
            return LeafNode("img", "", props)
        case _:
            raise Exception(f"Unhandled text type: {text_type}")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # Order matters: format first, then image, then link
    nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_node_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_node_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    current_block = []
    in_code_block = False
    lines = markdown.split('\n')

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                # closing code block
                current_block.append(line)
                blocks.append("\n".join(current_block).strip())
                current_block = []
                in_code_block = False
            else:
                # starting code block
                if current_block:
                    blocks.append("\n".join(current_block).strip())
                    current_block = []
                current_block.append(line)
                in_code_block = True
        elif in_code_block:
            current_block.append(line)
        elif line.strip() == "":
            # empty line ends current block if not in code block
            if current_block:
                blocks.append("\n".join(current_block).strip())
                current_block = []
        else:
            current_block.append(line)
    # append last block if any
    if current_block:
        blocks.append("\n".join(current_block).strip())
    return blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.strip('\n\r ').split('\n')
    # Detect fenced code block with ``` fences (allow optional trailing spaces)
    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return BlockType.CODE
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    if all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.strip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(rf"^{i+1}\. ", line.strip()) for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(line.strip() for line in lines if line.strip())
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level == 0 or level >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level:].strip()  # remove leading #s and any spaces
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    lines = block.split('\n')
    if lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    # Strip leading 4 spaces from all lines (if they have them)
    def strip_4_spaces(line):
        return line[4:] if line.startswith("    ") else line
    lines = [strip_4_spaces(line) for line in lines]
    text = '\n'.join(lines)
    if not text.endswith('\n'):
        text += '\n'
    child = LeafNode(None, text)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
