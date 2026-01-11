from enum import Enum
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE_TEXT = "code_text"
    LINKS = "links"
    IMAGES = "images"

class TextNode():
    def __init__(self, text: str, text_type: TextType = TextType.PLAIN, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type}, {self.url!r})"

def text_node_to_html_node(text_node: "TextNode") -> HTMLNode:
    if text_node.text_type == TextType.LINKS:
        if text_node.url is None:
            raise ValueError("URL must be provided for link text nodes")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="strong", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="em", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.IMAGES:
        if text_node.url is None:
            raise ValueError("URL must be provided for image text nodes")
        # Use empty value for <img> since it's a void element; alt is provided in props
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:  # Plain text
        return LeafNode(tag=None, value=text_node.text)