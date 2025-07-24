import unittest
from nodes.textnode import TextNode
from enum_types import TextType
from functions.nodehelpers import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_full_conversion(self):
        input_text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(input_text), expected)

    def test_plain_text(self):
        self.assertEqual(
            text_to_textnodes("Just plain text"),
            [TextNode("Just plain text", TextType.TEXT)]
        )

if __name__ == "__main__":
    unittest.main()
