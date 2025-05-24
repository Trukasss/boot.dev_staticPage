class HTMLNode():
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list["HTMLNode"] | None = None, 
            props: dict[str, str] | None = None
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
