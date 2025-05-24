from enum import Enum

class TextType(Enum):
    REGULAR = "regular" # Normal text
    BOLD = "bold" # **Bold text**
    ITALIC = "italic" # _Italic text_
    CODE = "code" # `Code text`
    LINK = "link" # Links, in this format: [anchor text](url)
    IMAGE = "image" # Images, in this format: ![alt text](url)


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
