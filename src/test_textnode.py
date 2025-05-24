import unittest
from textnode import TextNode, TextType, split_nodes_delimiter


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


if __name__ == "__main__":
    unittest.main()