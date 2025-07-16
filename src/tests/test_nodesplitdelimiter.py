import unittest
from nodes.textnode import TextNode, TextType
from functions.nodehelpers import split_node_delimiter  # adjust this import as needed

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("No formatting here", TextType.TEXT)
        result = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_single_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_node_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold(self):
        node = TextNode("**first** and **second**", TextType.TEXT)
        result = split_node_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_odd_number_of_delimiters(self):
        node = TextNode("This is **not closed properly", TextType.TEXT)
        result = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])  # unchanged due to unmatched delimiter

    def test_non_text_node_passthrough(self):
        node = TextNode("Already bold", TextType.BOLD)
        result = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_empty_parts_ignored(self):
        node = TextNode("Hello **** world", TextType.TEXT)
        result = split_node_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_mixed_text_and_format(self):
        node = TextNode("Start **mid** end **more** done", TextType.TEXT)
        result = split_node_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("mid", TextType.BOLD),
            TextNode(" end ", TextType.TEXT),
            TextNode("more", TextType.BOLD),
            TextNode(" done", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
