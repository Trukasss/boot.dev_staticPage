from enum import Enum
from typing import Literal, Any

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(
            self, 
            text: str, 
            text_type: TextType, 
            url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url 
    
    def __eq__(self, value: Any):
        if not isinstance(value, self.__class__):
            return False
        if (value.text == self.text
            and value.text_type == self.text_type
            and value.url == self.url):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        nb_delimiters = old_node.text.count(delimiter)
        if nb_delimiters == 0:
            new_nodes.append(old_node)
            continue
        if nb_delimiters % 2 != 0:
            raise ValueError(f"Unclosed delimiter '{delimiter}' in: {old_node.text}")
        parts = old_node.text.split(delimiter)
        for i, part in (enumerate(parts)):
            if not part:
                continue
            if i % 2 == 0: # outside delimiter
                new_nodes.append(TextNode(part, old_node.text_type))
            else: # inside delimiter
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text: str):
    from re import findall
    matches = findall(r"!\[(?P<text>.*?)\]\((?P<url>.*?)\)", text) # ![<text>](<url>)
    return matches


def extract_markdown_links(text: str):
    from re import findall
    matches = findall(r"\[(?P<text>.*?)\]\((?P<url>.*?)\)", text) # [<text>](<url>)
    return matches


def split_nodes_with_url(old_nodes: list[TextNode], strategy_type: Literal["image", "link"]):
    if strategy_type not in ["image", "link"]:
        raise ValueError(f"Unsupported split node strategy '{strategy_type}'")
    new_node_type = TextType.LINK if strategy_type == "link" else TextType.IMAGE
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if strategy_type == "link":
            matches = extract_markdown_links(node.text)
        else:
            matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        text_left = node.text
        for match in matches:
            match_text = match[0]
            match_url = match[1]
            if strategy_type == "link":
                sep = f"[{match_text}]({match_url})"
            else:
                sep = f"![{match_text}]({match_url})"
            parts = text_left.split(sep, 1)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            text_left = parts[1]
            new_nodes.append(TextNode(match_text, new_node_type, match_url))
        if text_left:
            new_nodes.append(TextNode(text_left, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = split_nodes_with_url(old_nodes, "image")
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = split_nodes_with_url(old_nodes, "link")
    return new_nodes


def text_to_textnodes(text: str):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes


def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks