import unittest
from functions.nodehelpers import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_paragraph(self):
        md = "This is a simple paragraph with **bold** and _italic_."
        self.assertEqual(
            markdown_to_blocks(md),
            ["This is a simple paragraph with **bold** and _italic_."]
        )

    def test_multiple_newlines(self):
        md = """
First block



Second block after many newlines


Third block
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "First block",
                "Second block after many newlines",
                "Third block"
            ]
        )

    def test_leading_and_trailing_newlines(self):
        md = """

# Heading


Paragraph in the middle


"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Heading",
                "Paragraph in the middle"
            ]
        )

    def test_block_with_internal_newlines(self):
        md = """Line one
Line two
Line three

Next block here"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Line one\nLine two\nLine three",
                "Next block here"
            ]
        )

    def test_only_whitespace_blocks(self):
        md = "   \n\n\t\n\nThis is actual content\n\n   "
        self.assertEqual(
            markdown_to_blocks(md),
            ["This is actual content"]
        )

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])

