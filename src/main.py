from textnode import TextNode
from htmlnode import HTMLNode

def main():
    node = TextNode("Hello, World!")
    print(node)
    html = HTMLNode(tag="p", children=[node])
    print(html)

if __name__ == "__main__":
    main()