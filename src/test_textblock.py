import unittest
from textblock import BlockType, block_to_block_type, block_to_html_node
from htmlnode import ParentNode, LeafNode


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_header(self):
        cases = [
            "# Title1",
            "## Title2",
            "### Title3",
            "#### Title4",
            "##### Title5",
            "###### Title6",
            "## Title2 with spaces",
            "# ## Title1 with two pounds",
            "# ############### Title1",

        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.HEADING)

    def test_block_to_not_header(self):
        cases = [
            "###No Space",
            "####### Title7",
            " #### Space in front",
            "Title### ",
        ]

        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertNotEqual(result, BlockType.HEADING)
                self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_code(self):
        cases = [
            "```\ncode block\n```",
            "```print('hi')```",
            "```def x():\n    pass\n```"
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.CODE)

    def test_block_to_not_code(self):
        cases = [
            "```\nnot closed",
            "not opened\n```",
            "`inline code`",
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertNotEqual(result, BlockType.CODE)
                self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_quote(self):
        cases = [
            ">quoteline",
            "> quote line",
            "> line 1\n> line 2\n> line 3"
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_not_quote(self):
        cases = [
            "regular line",
            "missing first\n> line 2\n> line 3"
            "> line 1\n> line 2\n missing last"
            "> line 1\nmissing middle\n> line 3"
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertNotEqual(result, BlockType.QUOTE)
                self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_unordered_list(self):
        cases = [
            "- only one item"
            "- item 1\n- item 2\n- item 3",
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_not_unordered_list(self):
        cases = [
            "-no space"
            "missing first\n- line 2\n- line 3"
            "- line 1\n- line 2\n missing last"
            "- line 1\nmissing middle\n- line 3"
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertNotEqual(result, BlockType.UNORDERED_LIST)
                self.assertEqual(result, BlockType.PARAGRAPH)
    

    def test_block_to_ordered_list(self):
        cases = [
            "1. First",
            "1. First\n2. Second\n3. Third",
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_not_ordered_list(self):
        cases = [
            "1.No Space",
            "1 No point",
            "1. First\n2.No Space\n3. Third",
            "1. First\n2. Second\n4. not a 3",
            "3. Third\n4. Fouth\n5. Fith",
            "1. First\ntext without number",
            "no numbers at all",
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertNotEqual(result, BlockType.ORDERED_LIST)
                self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_paragraph(self):
        cases = [
            "This is a paragraph.",
            "Just some text\nWith a second line",
            "Another\nblock\nof\ntext"
        ]
        for block in cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.PARAGRAPH)


class TestBlockToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_paragraph_to_html_node(self):
        pass
        cases = [
            (
                "This is a simple paragraph.",
                ParentNode("p", [
                    LeafNode(None, "This is a simple paragraph."),
                ])
            ),(
                "Another\nblock\nof\ntext",
                ParentNode("p", [
                    LeafNode(None, "Another\nblock\nof\ntext"),
                ])
            ),(
                "This is a paragraph with _italic text_ and a [link](https://to.link)",
                ParentNode("p", [
                    LeafNode(None, "This is a paragraph with "),
                    LeafNode("i", "italic text"),
                    LeafNode(None, " and a "),
                    LeafNode("a", "link", {"href": "https://to.link"}),
                ])
            ),
        ]
        for block, expected in cases:
            with self.subTest(block=block):
                result = block_to_html_node(block, block_type=BlockType.PARAGRAPH)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()