import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str):
    match = re.match(r"(?P<pounds>#*) ", block)
    if match:
        nb_pounds = len(match.group("pounds"))
        if nb_pounds > 0 and nb_pounds < 7:
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    is_ordered = True
    prev_num = 0
    for line in lines:
        match = re.match(r"(?P<num>\d+). ", line)
        if not match:
            is_ordered = False
            break
        num = int(match.group("num"))
        if prev_num + 1 != num:
            is_ordered = False
            break
        prev_num = num
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_to_html_node(block: str, block_type: BlockType):
    match block_type:
        case BlockType.PARAGRAPH:
            html_children = []
            text_nodes = text_to_textnodes(block)
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                leaf_node = LeafNode(html_node.tag, html_node.value, html_node.props)
                html_children.append(leaf_node)
            parent_node = ParentNode("div", html_children)
            return parent_node
        case BlockType.HEADING:
            html_children = []
            text_nodes = text_to_textnodes(block)
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                leaf_node = LeafNode(html_node.tag, html_node.value, html_node.props)
                html_children.append(leaf_node)
            parent_node = ParentNode("div", html_children)
        # case BlockType.CODE:
        #     pass
        # case BlockType.QUOTE:
        #     pass
        # case BlockType.UNORDERED_LIST:
        #     pass
        # case BlockType.ORDERED_LIST:
        #     pass
    # return html_nodes