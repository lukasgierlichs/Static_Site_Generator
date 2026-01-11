import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown: str) -> str:
    """
    Extracts the first H1 header from a markdown string.
    Returns the title text stripped of '#' and whitespace.
    Raises an Exception if no H1 header is found.
    """
    lines = markdown.split('\n')
    for line in lines:
        # Check if the line starts with '#' followed by content (not '##')
        if line.startswith("# "):
            return line[1:].strip()
        elif line.startswith("#"):
            # Handle cases where there might not be a space after '#'
            # but ensure it's not '##', '###', etc.
            if len(line) > 1 and line[1] != "#":
                return line[1:].strip()
            
    raise Exception("No H1 header found in the provided markdown.")

# Example usage:
# print(extract_title("# Hello"))  # Output: "Hello"
# print(extract_title("## Not a title\n# Actual Title"))  # Output: "Actual Title"

def generate_page(from_path, template_path, dest_path):
    """
    Generates a page by reading markdown content from 'from_path',
    applying a template from 'template_path', and writing the result to 'dest_path'.
    """
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    with open(from_path, 'r') as f:
        content = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    html_node = markdown_to_html_node(content)
    html = html_node.to_html()
    title = extract_title(content)
    final_page = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
    )

    # make sure dest_path directories exist and create them if not
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(final_page)
        print(f"Page generated at {dest_path}")
        # Log the path of the generated file
        print(f"Generated file: {dest_path}")
    print("Page generation complete.")
    return final_page
