from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(text: str) -> list[str]:
    """
    Converts raw markdown text (representing a full document) into a list of block strings.

    - Splits the document on double newlines ("\n\n").
    - Strips leading/trailing whitespace from each block.
    - Removes empty blocks created by excessive newlines.

    Returns an empty list for empty input.
    """
    if text == "":
        return []

    parts = [p.strip() for p in text.split("\n\n")]
    return [p for p in parts if p != ""]

def block_to_block_type(block: str) -> BlockType:
    """
    Determines the BlockType of a given markdown block string.
    Assume all leading and trailing whitespace has been stripped.

    - Headings start with 1-6 '#' characters.
    - Unordered lists start with '-'.
    - Ordered lists start with a number followed by a period and must be
      sequential starting at 1.
    - Code blocks are proper fenced blocks (start and end with ```).
    - Quotes start with '>'.
    - All other blocks are considered paragraphs.
    """
    # Treat empty or whitespace-only as paragraph
    if block.strip() == "":
        return BlockType.PARAGRAPH

    import re

    lines = block.splitlines()
    stripped = [ln.lstrip() for ln in lines]
    first = stripped[0]

    # Headings: 1-6 '#' followed by a space
    if re.match(r"^#{1,6}\s+", first):
        return BlockType.HEADING

    # Multiline fenced code block: starts with ``` and ends with ```
    if first.startswith("```") and stripped[-1].startswith("```") and len(lines) >= 2:
        return BlockType.CODE

    # Unordered list: every line must start with '- '
    if all(s.startswith("- ") for s in stripped) and len(stripped) >= 1:
        return BlockType.UNORDERED_LIST

    # Ordered list: use simple sequential prefix checks: 1., 2., 3., ...
    is_ordered = True
    for i, s in enumerate(stripped):
        if not s.startswith(f"{i+1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    # Quote: every line must start with '>' (possibly with trailing space)
    if all(s.startswith(">") for s in stripped) and len(stripped) >= 1:
        return BlockType.QUOTE

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str):
    """
    Convert a full markdown document into a single parent HTMLNode (<div>),
    whose children are block-level HTML nodes corresponding to the markdown.
    """
    # Delayed imports to avoid cycles
    from htmlnode import ParentNode, LeafNode
    from textnode import text_node_to_html_node
    from splitnodes import text_to_text_node

    def text_to_children(text: str):
        # Collapse internal newlines into spaces for inline parsing (except for code blocks)
        collapsed = " ".join(line.strip() for line in text.splitlines())
        text_nodes = text_to_text_node(collapsed)
        children = []
        for tn in text_nodes:
            # Use presentation tags for markdown rendering: <b> and <i>
            if tn.text_type.name == "BOLD":
                children.append(LeafNode("b", tn.text))
            elif tn.text_type.name == "ITALIC":
                children.append(LeafNode("i", tn.text))
            else:
                children.append(text_node_to_html_node(tn))
        # Ensure there's at least one child (empty paragraph)
        if not children:
            children = [LeafNode(None, "")]
        return children

    top_children = []
    blocks = markdown_to_blocks(markdown)

    for blk in blocks:
        btype = block_to_block_type(blk)
        lines = blk.splitlines()

        if btype == BlockType.PARAGRAPH:
            children = text_to_children(blk)
            top_children.append(ParentNode("p", children))

        elif btype == BlockType.HEADING:
            # Use first line only for heading, strip leading #'s
            first = lines[0].lstrip()
            import re
            m = re.match(r"^(#{1,6})\s+(.*)$", first)
            if m:
                level = len(m.group(1))
                content = m.group(2)
            else:
                level = 1
                content = first
            children = text_to_children(content)
            top_children.append(ParentNode(f"h{level}", children))
            # If the block contains additional lines (e.g., a following
            # quote or list on the next line without a blank line), process
            # the remainder as its own block so '# heading\n> quote' becomes
            # a heading followed by a quote.
            if len(lines) > 1:
                remainder = "\n".join(lines[1:]).strip()
                if remainder != "":
                    # Determine its type and process similarly to main loop
                    btype2 = block_to_block_type(remainder)
                    lines2 = remainder.splitlines()
                    if btype2 == BlockType.QUOTE:
                        parts = []
                        for ln in lines2:
                            s = ln.lstrip()
                            if s.startswith(">"):
                                parts.append(s[1:].lstrip())
                            else:
                                parts.append(s)
                        content2 = " ".join(parts)
                        children2 = text_to_children(content2)
                        top_children.append(ParentNode("blockquote", [ParentNode("p", children2)]))
                    elif btype2 == BlockType.PARAGRAPH:
                        top_children.append(ParentNode("p", text_to_children(remainder)))
                    elif btype2 == BlockType.UNORDERED_LIST:
                        items = []
                        for ln in lines2:
                            s = ln.lstrip()
                            if s.startswith("- "):
                                item_text = s[2:]
                            else:
                                item_text = s
                            items.append(ParentNode("li", text_to_children(item_text)))
                        top_children.append(ParentNode("ul", items))
                    elif btype2 == BlockType.ORDERED_LIST:
                        items = []
                        for ln in lines2:
                            s = ln.lstrip()
                            parts = s.split('. ', 1)
                            item_text = parts[1] if len(parts) > 1 else s
                            items.append(ParentNode("li", text_to_children(item_text)))
                        top_children.append(ParentNode("ol", items))
                    elif btype2 == BlockType.HEADING:
                        # Rare: nested heading on same block, fall back to paragraph
                        top_children.append(ParentNode("p", text_to_children(remainder)))
                    elif btype2 == BlockType.CODE:
                        # treat as code block
                        if len(lines2) >= 2 and lines2[0].lstrip().startswith("```") and lines2[-1].lstrip().startswith("```"):
                            inner2 = "\n".join(lines2[1:-1])
                            if inner2 != "":
                                inner2 = inner2 + "\n"
                        else:
                            inner2 = "\n".join(lines2)
                            if inner2 != "":
                                inner2 = inner2 + "\n"
                        code_node2 = LeafNode("code", inner2)
                        top_children.append(ParentNode("pre", [code_node2]))
        elif btype == BlockType.CODE:
            # Remove the opening and closing fence lines and keep content verbatim
            if len(lines) >= 2 and lines[0].lstrip().startswith("```") and lines[-1].lstrip().startswith("```"):
                inner = "\n".join(lines[1:-1])
                if inner != "":
                    inner = inner + "\n"
            else:
                inner = "\n".join(lines)
                if inner != "":
                    inner = inner + "\n"
            code_node = LeafNode("code", inner)
            top_children.append(ParentNode("pre", [code_node]))

        elif btype == BlockType.QUOTE:
            # Strip leading > and optional space from each line
            parts = []
            for ln in lines:
                s = ln.lstrip()
                if s.startswith(">"):
                    parts.append(s[1:].lstrip())
                else:
                    parts.append(s)
            content = " ".join(parts)
            children = text_to_children(content)
            top_children.append(ParentNode("blockquote", children))

        elif btype == BlockType.UNORDERED_LIST:
            items = []
            for ln in lines:
                s = ln.lstrip()
                if s.startswith("- "):
                    item_text = s[2:]
                else:
                    item_text = s
                li_children = text_to_children(item_text)
                items.append(ParentNode("li", li_children))
            top_children.append(ParentNode("ul", items))

        elif btype == BlockType.ORDERED_LIST:
            items = []
            for ln in lines:
                s = ln.lstrip()
                # Remove leading 'N. '
                parts = s.split('. ', 1)
                item_text = parts[1] if len(parts) > 1 else s
                li_children = text_to_children(item_text)
                items.append(ParentNode("li", li_children))
            top_children.append(ParentNode("ol", items))

    # If there are no blocks (empty document) ensure the div still has
    # a child so ParentNode.to_html() can render an empty div rather than
    # raising. An empty leaf with empty value renders as empty content.
    if not top_children:
        top_children = [LeafNode(None, "")]

    # Wrap all blocks in a single div
    return ParentNode("div", top_children)
