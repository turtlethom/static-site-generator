from textnode import TextType
from htmlnode import LeafNode

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
