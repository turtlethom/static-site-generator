import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("div", "Hello world", "p", {"class": "container"})
        node2 = HTMLNode("div", "Hello world", "p", {"class": "container"})
        self.assertEqual(node1, node2)

    def test_repr(self):
        node = HTMLNode("div", "Hello", None, {"id": "main"})
        expected = "HTMLNode(div, Hello, None, {'id': 'main'})"
        self.assertEqual(repr(node), expected)

    def test_props_to_html(self):
        node = HTMLNode("a", "Link", None, {"href": "https://example.com", "target": "_blank"})
        props_str = node.props_to_html()
        # Since dictionary order isn't guaranteed, we check both possibilities
        options = [
            ' href="https://example.com" target="_blank"',
            ' target="_blank" href="https://example.com"'
        ]
        self.assertIn(props_str, options)

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Hello", None, None)
        self.assertEqual(node.props_to_html(), "")

class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")
    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_missing_tag_raises(self):
        child_node = LeafNode("p", "text")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child_node]).to_html()
        self.assertIn("must have a tag", str(context.exception))

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", []).to_html()
        self.assertIn("must have at least one child", str(context.exception))


    def test_to_html_with_props(self):
        child_node = LeafNode("span", "text")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>text</span></div>'
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "Hello")
        child2 = LeafNode("p", "World")
        parent = ParentNode("section", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<section><p>Hello</p><p>World</p></section>"
        )

    def test_deeply_nested_structure(self):
        leaf = LeafNode("em", "text")
        inner = ParentNode("i", [leaf])
        middle = ParentNode("span", [inner])
        outer = ParentNode("div", [middle])
        self.assertEqual(
            outer.to_html(),
            "<div><span><i><em>text</em></i></span></div>"
        )
if __name__ == "__main__":
    unittest.main()
