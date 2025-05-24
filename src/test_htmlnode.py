import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from enum import Enum


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "highlight"})
        self.assertEqual(node.props_to_html(), ' class="highlight"')

    def test_props_to_html_multiple_props(self):
        props = {"id": "main", "class": "container"}
        node = HTMLNode(props=props)
        result = node.props_to_html()
        self.assertEqual(result, ' id="main" class="container"')

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "text"})
        expecteded = "HTMLNode(tag=p, value=Hello, children=[], props={'class': 'text'})"
        self.assertEqual(repr(node), expecteded)

    def test_to_html_raises(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)
    
    def test_to_html_raw(self):
        node = LeafNode(None, "raw text")
        expected = "raw text"
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_node_raw_text_with_props(self):
        node = LeafNode(None, "raw text", {"class": "note"})
        self.assertEqual(node.to_html(), "raw text")
    
    def test_to_html_no_value(self):
        node = LeafNode("p", None) # type: ignore # it is supposed to be an error
        with self.assertRaises(ValueError):
            node.to_html()
    

class TestParentNode(unittest.TestCase):
    def test_to_html_without_tag(self):
        child_node = LeafNode(None, "raw text")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_without_tag2(self):
        child_node = LeafNode(None, "raw text")
        parent_node = ParentNode(None, [child_node]) #type: ignore
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_without_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_children2(self):
        parent_node = ParentNode("div", None) #type: ignore
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_with_invalid_child(self):
        parent = ParentNode("div", ["not a node"])  # type: ignore
        with self.assertRaises(TypeError):
            parent.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_node_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>child</span></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_htl_without_grandchildren(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
   

class TestTextNode_to_HTMLNode(unittest.TestCase):
    def test_all_text_types(self):
        cases = [
            (TextNode("text", TextType.TEXT), (None, "text", None, None)),
            (TextNode("bold", TextType.BOLD), ("b", "bold", None, None)),
            (TextNode("italic", TextType.ITALIC), ("i", "italic", None, None)),
            (TextNode("code", TextType.CODE), ("code", "code", None, None)),
            (TextNode("link", TextType.LINK, "url"), ("a", "link", None, {"href": "url"})),
            (TextNode("img", TextType.IMAGE, "url"), ("img", "", None, {"src": "url", "alt": "img"})),
        ]
        for node, expected in cases:
            with self.subTest(node=node):
                html = text_node_to_html_node(node)
                self.assertEqual((html.tag, html.value, html.children, html.props), expected)

    def test_unsupported_text_type(self):
        class FakeTextType(Enum):
            UNKNOWN = "unknown"
        node = TextNode("Text", FakeTextType.UNKNOWN)  # type: ignore
        with self.assertRaises(AttributeError):
            text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()