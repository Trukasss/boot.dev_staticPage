from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    TEXT = "text"
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
    
    def __eq__(self, value):
        if not isinstance(value, self.__class__):
            return False
        if (value.text == self.text
            and value.text_type == self.text_type
            and value.url == self.url):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def point_to_error(input_str: str, error_index: int, length: int = 1) -> str:
    pointer_line = " " * error_index + "^" * length
    return f"{input_str}\n{pointer_line}"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
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
        
        

node = TextNode("`This` is text with a `code block` `word`", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
for n in new_nodes:
    print(n)