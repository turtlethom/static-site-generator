from enum import Enum

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f"{key}=\"{value}\"" for key, value in self.props.items())

    def __eq__(self, other):
        check_tag = self.tag == other.tag
        check_value = self.value == other.value

        check_children = True if len(self.children) else False
        for child in self.children:
            if not child in other.children:
                check_children = False

        check_props = True
        for prop in self.props:
            if prop not in self.props or self.props[prop] != other.props[prop]:
                check_props = False

        return check_tag and check_value and check_children and check_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{value}"
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have at least one child")
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"

