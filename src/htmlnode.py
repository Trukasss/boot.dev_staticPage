from textnode import TextNode, TextType


class HTMLNode():
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list["HTMLNode"] | None = None, 
            props: dict | None = None
            ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join([f'{key}="{self.props[key]}"' for key in self.props])
    
    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    def __eq__(self, value):
        if not isinstance(value, HTMLNode):
            return False
        if (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        ):
            return True
        return False
    

class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag: str | None, 
            value: str, 
            props: dict[str, str] | None = None
            ) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf Node must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
            self, 
            tag: str, 
            children: list[HTMLNode], 
            props: dict[str, str] | None = None
            ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        if not all(isinstance(child, HTMLNode) for child in self.children):
            raise TypeError("All children must be instances of HTMLNode")
        result = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            result += node.to_html()
        result += f"</{self.tag}>"
        return result


def text_node_to_html_node(text_node: TextNode):
    tt = text_node.text_type
    match tt:
        case TextType.TEXT:
            return HTMLNode(value=text_node.text)
        case TextType.BOLD:
            return HTMLNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return HTMLNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return HTMLNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return HTMLNode(
                tag="a", 
                value=text_node.text, 
                props={"href": text_node.url},
                )
        case TextType.IMAGE:
            return HTMLNode(
                tag="img", 
                value="", 
                props={
                    "src": text_node.url,
                    "alt": text_node.text
                    },
                )
        case _:
            raise AttributeError(f"Unsupported TextType enum value {text_node.text_type}")