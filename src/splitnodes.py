from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Simplified splitter: operates on a flat list and returns a flat list.

    - Non-plain nodes are passed through unchanged.
    - If `delimiter` is empty, the original nodes are returned.
    - An exact node matching the delimiter becomes a TextNode with `text_type`.
      For opening delimiters that require a matching closer (e.g., '['), a
      missing closer later in the sequence raises ValueError.
    - For plain nodes containing the delimiter, the node text is split on the
      delimiter. Parts alternate plain/formatted with odd-numbered parts
      becoming `text_type`. Empty parts are skipped. If number of parts is
      even, that's an unclosed formatted section and a ValueError is raised.
    """
    if delimiter == "":
        return list(old_nodes)

    new_nodes = []
    CLOSING = {"[": "]", "(": ")", "{": "}", "<": ">"}

    for idx, node in enumerate(old_nodes):
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        # exact delimiter node
        if node.text == delimiter:
            if delimiter in CLOSING:
                closing = CLOSING[delimiter]
                if not any(nd.text == closing for nd in old_nodes[idx + 1 :]):
                    raise ValueError(
                        f"Unmatched opening delimiter '{delimiter}': missing closing '{closing}'"
                    )
            new_nodes.append(TextNode(delimiter, text_type))
            continue

        # delimiter inside text
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    # Splits nodes by markdown image syntax (e.g. ![alt](url)).
    # Operates on runs of plain text nodes so images that span node boundaries
    # (e.g., '!', '[', 'alt', ']', '(', 'url', ')') are detected.
    new_nodes = []
    buffer = []

    def flush_buffer():
        if not buffer:
            return
        combined = "".join(n.text for n in buffer)
        matches = extract_markdown_images(combined)
        if not matches:
            # no images, preserve original nodes
            new_nodes.extend(buffer)
        else:
            remaining = combined
            for alt, url in matches:
                token = f"![{alt}]({url})"
                pre, _, post = remaining.partition(token)
                if pre:
                    new_nodes.append(TextNode(pre, TextType.PLAIN))
                # store alt and url separately
                new_nodes.append(TextNode(alt, TextType.IMAGES, url))
                remaining = post
            if remaining:
                new_nodes.append(TextNode(remaining, TextType.PLAIN))
        buffer.clear()

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            flush_buffer()
            new_nodes.append(node)
            continue
        buffer.append(node)

    flush_buffer()
    return new_nodes

def split_nodes_link(old_nodes):
    # Splits nodes by markdown link syntax (e.g. [text](url)).
    # Operates on runs of plain text nodes so links that span node boundaries
    # are detected.
    new_nodes = []
    buffer = []

    def flush_buffer():
        if not buffer:
            return
        combined = "".join(n.text for n in buffer)
        matches = extract_markdown_links(combined)
        if not matches:
            new_nodes.extend(buffer)
        else:
            remaining = combined
            for label, url in matches:
                token = f"[{label}]({url})"
                pre, _, post = remaining.partition(token)
                if pre:
                    new_nodes.append(TextNode(pre, TextType.PLAIN))
                new_nodes.append(TextNode(label, TextType.LINKS, url))
                remaining = post
            if remaining:
                new_nodes.append(TextNode(remaining, TextType.PLAIN))
        buffer.clear()

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            flush_buffer()
            new_nodes.append(node)
            continue
        buffer.append(node)

    flush_buffer()
    return new_nodes

def text_to_text_node(text: str) -> list[TextNode]:
    """
    Converts a plain text string into a list of TextNode instances.

    - Empty string yields an empty list.
    - Otherwise returns a sequence of TextNodes representing plain and formatted parts.
    """
    if text == "":
        return []

    # Start with a single plain text node
    nodes = [TextNode(text, TextType.PLAIN)]

    # Apply formatting splitters in order
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)

    # Apply image and link splitters
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
