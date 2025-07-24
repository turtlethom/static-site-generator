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
        # Text node (no tag)
        if not self.tag:
            if self.value is None:
                raise ValueError("Text nodes must have a value")
            return f"{self.value}"

        # Self-closing HTML tags
        self_closing_tags = {'img', 'br', 'hr', 'input', 'meta', 'link'}
        if self.tag in self_closing_tags:
            return f"<{self.tag}{self.props_to_html()} />"

        # Regular tags
        if self.value is None:
            raise ValueError(f"Leaf node <{self.tag}> must have a value")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

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

