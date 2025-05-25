import unittest
from textnode import (
    TextNode, 
    TextType, 
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestTexNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("text", TextType.BOLD)
        node2 = TextNode("text", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_eq_with_url(self):
        node1 = TextNode("text", TextType.CODE, "https://test.com")
        node2 = TextNode("text", TextType.CODE, "https://test.com")
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        node1 = TextNode("text 1", TextType.ITALIC)
        node2 = TextNode("text 2", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    
    def test_neq_text_type(self):
        node1 = TextNode("text", TextType.IMAGE)
        node2 = TextNode("text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    
    def test_neq_url(self):
        node1 = TextNode("text", TextType.TEXT, "https://url1.com")
        node2 = TextNode("text", TextType.TEXT, "https://url2.com")
        self.assertNotEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("Example", TextType.CODE)
        self.assertEqual(repr(node), "TextNode(Example, code, None)")

    def test_repr_with_url(self):
        node = TextNode("Example", TextType.LINK, url="http://example.com")
        self.assertEqual(repr(node), "TextNode(Example, link, http://example.com)")


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        nodes = [TextNode("No formatting here", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, nodes)

    def test_balanced_delimiters(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_unbalanced_delimiters_raises(self):
        nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_multiple_delimiters(self):
        nodes = [TextNode("**bold** and **strong**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_nested_non_text_nodes_are_ignored(self):
        non_text_node = TextNode("<b>ignore me</b>", TextType.BOLD)
        result = split_nodes_delimiter([non_text_node], "**", TextType.BOLD)
        self.assertEqual(result, [non_text_node])

    def test_empty_parts_are_skipped(self):
        nodes = [TextNode("****", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = []  # All parts are empty
        self.assertEqual(result, expected)

    def test_text_with_leading_and_trailing_delimiters(self):
        nodes = [TextNode("**start** middle **end**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("start", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("Hello **world**", TextType.TEXT),
            TextNode("Not affected", TextType.ITALIC),
            TextNode("**Again** yes", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("Not affected", TextType.ITALIC),
            TextNode("Again", TextType.BOLD),
            TextNode(" yes", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


class TestExtractMarkdownImage(unittest.TestCase):
    def test_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://www.domain.com/image1.png) space"
        )
        self.assertListEqual([("image1", "https://www.domain.com/image1.png")], matches)
    
    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://www.domain.com/image1.png), this is the seconde text image ![image2](https://www.domain.com/image2.png)"
        )
        self.assertListEqual([
            ("image1", "https://www.domain.com/image1.png"),
            ("image2", "https://www.domain.com/image2.png"),
            ], matches)
    
    def test_only_image(self):
        matches = extract_markdown_images(
            "![image](https://www.domain.com/image.png)"
        )
        self.assertListEqual([("image", "https://www.domain.com/image.png")], matches)
    
    def test_only_images(self):
        matches = extract_markdown_images(
            "![image1](https://www.domain.com/image1.png)![image2](https://www.domain.com/image2.png)"
        )
        self.assertListEqual([
            ("image1", "https://www.domain.com/image1.png"),
            ("image2", "https://www.domain.com/image2.png"),
            ], matches)
    
    def test_no_images(self):
        texts = [
            "This is simple text",
            "without exlamation point [image](url)"
            "with spaces ! [image](url)",
            "with spaces ![image] (url)",
            "without url ![image]",
            "without image !(url)",
        ]
        for text in texts:
            with self.subTest(text=text):
                matches = extract_markdown_images(text)
                self.assertListEqual(matches, [])
    
    def test_empty(self):
        texts = [
            "![]()",
            "text in front ![]()",
            "![]() text at the end",
            "text in front ![]() text at the end",
            "nospaces![]()nospaces",
        ]
        for text in texts:
            with self.subTest(text=text):
                matches = extract_markdown_images(text)
                self.assertListEqual(matches, [("", "")])
    
    def test_empties(self):
        texts = [
            "![]()![]()",
            "text in front ![]()![]()",
            "![]()![]() text at the end",
            "![]()text in the middle![]()",
            "text in front ![]()text in the middle![]() text at the end",
        ]
        for text in texts:
            with self.subTest(text=text):
                matches = extract_markdown_images(text)
                self.assertListEqual(matches, [("", ""), ("", "")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        matches = extract_markdown_links(
            "This is text with an [link1](https://www.domain.com/link1) space"
        )
        self.assertListEqual([("link1", "https://www.domain.com/link1")], matches)
    
    def test_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with an [link1](https://www.domain.com/link1), this is the seconde text link [link2](https://www.domain.com/link2)"
        )
        self.assertListEqual([
            ("link1", "https://www.domain.com/link1"),
            ("link2", "https://www.domain.com/link2"),
            ], matches)
    
    def test_only_link(self):
        matches = extract_markdown_links(
            "[link](https://www.domain.com/link)"
        )
        self.assertListEqual([("link", "https://www.domain.com/link")], matches)
    
    def test_only_links(self):
        matches = extract_markdown_links(
            "[link1](https://www.domain.com/link1)[link2](https://www.domain.com/link2)"
        )
        self.assertListEqual([
            ("link1", "https://www.domain.com/link1"),
            ("link2", "https://www.domain.com/link2"),
            ], matches)
    
    def test_no_links(self):
        texts = [
            "This is simple text",
            "with spaces [link] (url)",
            "without url [link]",
            "without link (url)",
        ]
        for text in texts:
            with self.subTest(text=text):
                matches = extract_markdown_links(text)
                self.assertListEqual(matches, [])
    
    def test_empty(self):
        texts = [
            "[]()",
            "text in front []()",
            "[]() text at the end",
            "text in front []() text at the end",
            "nospaces[]()nospaces",
        ]
        for text in texts:
            with self.subTest(text=text):
                matches = extract_markdown_links(text)
                self.assertListEqual(matches, [("", "")])
    
    def test_empties(self):
        texts = [
            "[]()[]()",
            "text in front []()[]()",
            "[]()[]() text at the end",
            "[]()text in the middle[]()",
            "text in front []()text in the middle[]() text at the end",
        ]
        for text in texts:
            with self.subTest(text=text):
                matches = extract_markdown_links(text)
                self.assertListEqual(matches, [("", ""), ("", "")])
    

if __name__ == "__main__":
    unittest.main()