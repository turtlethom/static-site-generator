import unittest
from functions.nodehelpers import block_to_block_type
from enum_types import BlockType

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading 1"),
            BlockType.HEADING,
        )
        self.assertEqual(
            block_to_block_type("###### Heading 6"),
            BlockType.HEADING,
        )

    def test_code_block(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> Another line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "Just a regular paragraph of text without any formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_no_space(self):
        block = "##HeadingWithoutSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_bad_format(self):
        block = "-good\n- bad format"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_numbers(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_with_missing_symbol(self):
        block = "> valid quote line\ninvalid line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
