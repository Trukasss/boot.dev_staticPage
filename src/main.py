from textnode import TextNode, TextType


def main():
    textNode = TextNode("This is some anchor text", TextType.REGULAR, "https://www.boot.dev")
    print(textNode)


if __name__ == "__main__":
    main()