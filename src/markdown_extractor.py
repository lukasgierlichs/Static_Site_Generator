import re

def extract_markdown_images(text):
    """
    Extracts markdown image links from the given text.

    Args:
        text (str): The input text containing markdown image links.

    Returns:
        list of tuples: A list of tuples where each tuple contains the alt text and URL of the image.
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown links from the given text.

    Args:
        text (str): The input text containing markdown links.
    Returns:
        list of tuples: A list of tuples where each tuple contains the link text and URL.
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches