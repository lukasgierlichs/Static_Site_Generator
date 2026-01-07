from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits a list of TextNode objects into multiple lists based on a specified delimiter.

    Args:
        old_nodes (list of TextNode): The original list of TextNode objects to be split.
        delimiter (str): The delimiter string used to split the text nodes.
        text_type (TextType): The TextType to assign to the delimiter nodes.

    Returns:
        list of list of TextNode: A list containing sublists of TextNode objects, split by the delimiter.
    """
    new_nodes = []
    current_sublist = []

    PUNCTUATION = set('. , ! ? : ;'.split())
    # mapping of opening -> closing delimiters
    CLOSING = {'[': ']', '(': ')', '{': '}', '<': '>'}

    n = len(old_nodes)
    i = 0
    while i < n:
        node = old_nodes[i]

        # If node is not plain text, don't attempt splitting -- just append as-is
        if node.text_type != TextType.PLAIN:
            current_sublist.append(node)
            i += 1
            continue

        # empty delimiter -> no splitting
        if delimiter == "":
            current_sublist.append(node)
            i += 1
            continue

        # Direct match of delimiter token (e.g., a node that is exactly "[")
        if node.text == delimiter:
            # If delimiter is an opening delimiter that has a different closing
            # (e.g., '[' -> ']'), ensure a matching closing delimiter exists.
            if delimiter in CLOSING:
                closing = CLOSING[delimiter]
                found = any(nd.text == closing for nd in old_nodes[i+1:])
                if not found:
                    raise ValueError(f"Unmatched opening delimiter '{delimiter}': missing closing '{closing}'")

            if current_sublist:
                new_nodes.append(current_sublist)
                current_sublist = []
            delimiter_node = TextNode(text=delimiter, text_type=text_type)
            new_nodes.append([delimiter_node])
            i += 1
            continue

        # Special-case: ensure closing square bracket ']' starts its own sublist
        if node.text == "]":
            if current_sublist:
                new_nodes.append(current_sublist)
                current_sublist = []
            new_nodes.append([node])
            i += 1
            continue

        # If delimiter occurs inside the node text, split the node into parts
        if delimiter in node.text:
            parts = node.text.split(delimiter)
            # Interleave parts with delimiter nodes
            for j, part in enumerate(parts):
                if part:
                    current_sublist.append(TextNode(part, TextType.PLAIN))
                # After each part except the last, we have a delimiter
                if j != len(parts) - 1:
                    if current_sublist:
                        new_nodes.append(current_sublist)
                        current_sublist = []
                    new_nodes.append([TextNode(delimiter, text_type)])
            i += 1
            continue

        # Handle punctuation separation from previous formatting
        if node.text in PUNCTUATION and current_sublist and current_sublist[-1].text_type != text_type:
            new_nodes.append(current_sublist)
            new_nodes.append([node])
            current_sublist = []
            i += 1
            continue

        # Otherwise, just append node to current sublist
        current_sublist.append(node)
        i += 1

    if current_sublist:
        new_nodes.append(current_sublist)

    return new_nodes

def split_nodes_image(old_nodes):
    """Splits nodes by markdown image syntax (e.g. ![alt](url))."""
    # Use extractor-based splitting per-node so we handle multiple images
    # inside a single TextNode and avoid creating empty TextNodes.
    def make_token(alt, url):
        return f"![{alt}]({url})"

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append([node])
            continue

        text = node.text
        matches = extract_markdown_images(text)
        if not matches:
            new_nodes.append([node])
            continue

        remaining = text
        for alt, url in matches:
            token = make_token(alt, url)
            pre, _, post = remaining.partition(token)
            if pre:
                new_nodes.append([TextNode(pre, TextType.PLAIN)])
            new_nodes.append([TextNode(token, TextType.IMAGES)])
            remaining = post

        if remaining:
            new_nodes.append([TextNode(remaining, TextType.PLAIN)])

    return new_nodes

def split_nodes_link(old_nodes):
    """Splits nodes by markdown link syntax (e.g. [text](url))."""
    def make_token(text_label, url):
        return f"[{text_label}]({url})"

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append([node])
            continue

        text = node.text
        matches = extract_markdown_links(text)
        if not matches:
            new_nodes.append([node])
            continue

        remaining = text
        for label, url in matches:
            token = make_token(label, url)
            pre, _, post = remaining.partition(token)
            if pre:
                new_nodes.append([TextNode(pre, TextType.PLAIN)])
            new_nodes.append([TextNode(token, TextType.LINKS)])
            remaining = post

        if remaining:
            new_nodes.append([TextNode(remaining, TextType.PLAIN)])

    return new_nodes