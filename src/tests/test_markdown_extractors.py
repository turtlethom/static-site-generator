import unittest
from functions.extracters import extract_markdown_images, extract_markdown_links, extract_title

class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](url1) and ![two](url2)"
        )
        self.assertListEqual(
            [("one", "url1"), ("two", "url2")], matches
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
            "No images here, just text and maybe [a link](https://example.com)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "A link to [Google](https://www.google.com)"
        )
        self.assertListEqual(
            [("Google", "https://www.google.com")], matches
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Links: [first](url1) and [second](url2)"
        )
        self.assertListEqual(
            [("first", "url1"), ("second", "url2")], matches
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "No links, just ![images](img.png)"
        )
        self.assertListEqual([], matches)

    def test_single_h1(self):
        self.assertEqual(extract_title("# Hello World"), "Hello World")

    def test_h1_with_extra_spaces(self):
        self.assertEqual(extract_title("#    Trim Me   "), "Trim Me")

    def test_multiple_headings(self):
        markdown = """
## Subtitle
# Main Title
### Another
"""
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## Only Subtitle\n### Smaller Heading")

    def test_h1_in_later_line(self):
        markdown = """
Some intro text

# Real Title
"""
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_h1_with_trailing_spaces(self):
        self.assertEqual(extract_title("# Heading   "), "Heading")

if __name__ == "__main__":
    unittest.main()
