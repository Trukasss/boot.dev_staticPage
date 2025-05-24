import unittest
from textnode import TextNode, TextType


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
        node1 = TextNode("text", TextType.REGULAR, "https://url1.com")
        node2 = TextNode("text", TextType.REGULAR, "https://url2.com")
        self.assertNotEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("Example", TextType.CODE)
        self.assertEqual(repr(node), "TextNode(Example, code, None)")

    def test_repr_with_url(self):
        node = TextNode("Example", TextType.LINK, url="http://example.com")
        self.assertEqual(repr(node), "TextNode(Example, link, http://example.com)")


if __name__ == "__main__":
    unittest.main()