import unittest
from nodes.textnode import TextNode
from enum_types import TextType
from functions.splitters import split_node_delimiter, split_nodes_image, split_nodes_link

class TestMarkdownSplitters(unittest.TestCase):
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
    def test_split_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                ],
                new_nodes,
            )
    def test_split_image_none(self):
        node = TextNode("This has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_only(self):
        node = TextNode("![solo](https://img.com/solo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("solo", TextType.IMAGE, "https://img.com/solo.png")],
            new_nodes,
        )

    def test_split_image_edge_text(self):
        node = TextNode("![img1](url1) end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_none(self):
        node = TextNode("Plain text without links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_only(self):
        node = TextNode("[label](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("label", TextType.LINK, "url")],
            new_nodes,
        )

    def test_split_link_trailing_text(self):
        node = TextNode("[go](there) and more", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("go", TextType.LINK, "there"),
                TextNode(" and more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_and_image_same_node(self):
        node = TextNode("Link [a](b) and ![img](c)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        # Should only handle the link, not the image
        self.assertListEqual(
            [
                TextNode("Link ", TextType.TEXT),
                TextNode("a", TextType.LINK, "b"),
                TextNode(" and ![img](c)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_ignores_non_text_nodes(self):
        node1 = TextNode("![img](url)", TextType.TEXT)
        node2 = TextNode("ignore me", TextType.LINK, "url")
        result = split_nodes_image([node1, node2])
        self.assertEqual(result[1], node2)
        result2 = split_nodes_link([node1, node2])
        self.assertEqual(result2[1], node2)

if __name__ == "__main__":
    unittest.main()
