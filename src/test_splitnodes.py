import unittest
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_text_node
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        nodes = [
            TextNode("Hello", TextType.PLAIN),
            TextNode(",", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("World", TextType.PLAIN),
            TextNode("!", TextType.PLAIN),
            TextNode("\n", TextType.PLAIN),
            TextNode("This", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("is", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("a", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("test.", TextType.PLAIN),
        ]
        delimiter = "\n"
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("Hello", TextType.PLAIN),
            TextNode(",", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("World", TextType.PLAIN),
            TextNode("!", TextType.PLAIN),
            TextNode("\n", text_type),
            TextNode("This", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("is", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("a", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("test.", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)
    
    def test_no_delimiter(self):
        nodes = [
            TextNode("No", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("delimiter", TextType.PLAIN),
        ]
        delimiter = "\n"
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("No", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("delimiter", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)
    
    def test_consecutive_delimiters(self):
        nodes = [
            TextNode("Line1", TextType.PLAIN),
            TextNode("\n", TextType.PLAIN),
            TextNode("\n", TextType.PLAIN),
            TextNode("Line2", TextType.PLAIN),
        ]
        delimiter = "\n"
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("Line1", TextType.PLAIN),
            TextNode("\n", text_type),
            TextNode("\n", text_type),
            TextNode("Line2", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)
    
    def test_delimiter_at_start_and_end(self):
        nodes = [
            TextNode("\n", TextType.PLAIN),
            TextNode("Content", TextType.PLAIN),
            TextNode("\n", TextType.PLAIN),
        ]
        delimiter = "\n"
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("\n", text_type),
            TextNode("Content", TextType.PLAIN),
            TextNode("\n", text_type),
        ]

        self.assertEqual(result, expected)
    
    def test_empty_input(self):
        nodes = []
        delimiter = "\n"
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = []

        self.assertEqual(result, expected)
    
    def test_only_delimiters(self):
        nodes = [
            TextNode("\n", TextType.PLAIN),
            TextNode("\n", TextType.PLAIN),
            TextNode("\n", TextType.PLAIN),
        ]
        delimiter = "\n"
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("\n", text_type),
            TextNode("\n", text_type),
            TextNode("\n", text_type),
        ]

        self.assertEqual(result, expected)
    
    def test_delimiter_not_in_nodes(self):
        nodes = [
            TextNode("Just", TextType.PLAIN),
            TextNode("some", TextType.PLAIN),
            TextNode("text.", TextType.PLAIN),
        ]
        delimiter = ","
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("Just", TextType.PLAIN),
            TextNode("some", TextType.PLAIN),
            TextNode("text.", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)

    def test_empty_string_delimiter(self):
        nodes = [
            TextNode("A", TextType.PLAIN),
            TextNode("B", TextType.PLAIN),
        ]
        delimiter = ""
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("A", TextType.PLAIN),
            TextNode("B", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)

    # test different types of delimiters
    # e.g., markdown to html conversion context
    def test_markdown_delimiter(self):
        nodes = [
            TextNode("This", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("is", TextType.PLAIN),
            TextNode(" ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode("!", TextType.PLAIN),
        ]
        delimiter = " "
        text_type = TextType.PLAIN

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("This", TextType.PLAIN),
            TextNode(" ", text_type),
            TextNode("is", TextType.PLAIN),
            TextNode(" ", text_type),
            TextNode("bold", TextType.BOLD),
            TextNode("!", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)

    def test_star_delimiter(self):
        nodes = [
            TextNode("*", TextType.PLAIN),
            TextNode("italic", TextType.PLAIN),
            TextNode("*", TextType.PLAIN),
        ]
        delimiter = "*"
        text_type = TextType.ITALIC

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("*", text_type),
            TextNode("italic", TextType.PLAIN),
            TextNode("*", text_type),
        ]

        self.assertEqual(result, expected)

    def test_double_star_delimiter(self):
        nodes = [
            TextNode("This", TextType.PLAIN),
            TextNode("**", TextType.PLAIN),
            TextNode("bold", TextType.PLAIN),
            TextNode("**", TextType.PLAIN),
            TextNode("text", TextType.PLAIN),
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("This", TextType.PLAIN),
            TextNode("**", text_type),
            TextNode("bold", TextType.PLAIN),
            TextNode("**", text_type),
            TextNode("text", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)

    def test_backtick_delimiter(self):
        nodes = [
            TextNode("`", TextType.PLAIN),
            TextNode("print('x')", TextType.PLAIN),
            TextNode("`", TextType.PLAIN),
        ]
        delimiter = "`"
        text_type = TextType.CODE_TEXT

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("`", text_type),
            TextNode("print('x')", TextType.PLAIN),
            TextNode("`", text_type),
        ]

        self.assertEqual(result, expected)

    def test_link_delimiter(self):
        nodes = [
            TextNode("[", TextType.PLAIN),
            TextNode("link text", TextType.PLAIN),
            TextNode("]", TextType.PLAIN),
            TextNode("(", TextType.PLAIN),
            TextNode("http://example.com", TextType.PLAIN),
            TextNode(")", TextType.PLAIN),
        ]
        delimiter = "["
        text_type = TextType.LINKS

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("[", text_type),
            TextNode("link text", TextType.PLAIN),
            TextNode("]", TextType.PLAIN),
            TextNode("(", TextType.PLAIN),
            TextNode("http://example.com", TextType.PLAIN),
            TextNode(")", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)

    def test_closing_bracket_split(self):
        # Explicit test to ensure closing bracket is its own sublist
        nodes = [
            TextNode("link", TextType.PLAIN),
            TextNode("[", TextType.PLAIN),
            TextNode("text", TextType.PLAIN),
            TextNode("]", TextType.PLAIN),
        ]
        delimiter = "["
        text_type = TextType.LINKS

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("link", TextType.PLAIN),
            TextNode("[", text_type),
            TextNode("text", TextType.PLAIN),
            TextNode("]", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)

    def test_image_delimiter(self):
        nodes = [
            TextNode("!", TextType.PLAIN),
            TextNode("[", TextType.PLAIN),
            TextNode("alt", TextType.PLAIN),
            TextNode("]", TextType.PLAIN),
            TextNode("(", TextType.PLAIN),
            TextNode("url", TextType.PLAIN),
            TextNode(")", TextType.PLAIN),
        ]
        delimiter = "!"
        text_type = TextType.IMAGES

        result = split_nodes_image(nodes)

        expected = [
            TextNode("alt", TextType.IMAGES, "url"),
        ]

        self.assertEqual(result, expected)

    def test_unmatched_opening_raises(self):
        nodes = [
            TextNode("[", TextType.PLAIN),
            TextNode("text", TextType.PLAIN),
        ]
        delimiter = "["
        text_type = TextType.LINKS

        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, delimiter, text_type)

    def test_non_plain_nodes_not_split(self):
        nodes = [
            TextNode("open", TextType.PLAIN),
            TextNode("*", TextType.BOLD),  # not plain, should not be treated as delimiter
            TextNode("close", TextType.PLAIN),
        ]
        delimiter = "*"
        text_type = TextType.ITALIC

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            TextNode("open", TextType.PLAIN),
            TextNode("*", TextType.BOLD),
            TextNode("close", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)
    
    def test_split_nodes_link(self):
        nodes = [
            TextNode("This is a [link](http://example.com) in text.", TextType.PLAIN),
        ]

        result = split_nodes_link(nodes)

        expected = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("link", TextType.LINKS, "http://example.com"),
            TextNode(" in text.", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)
    
    def test_no_links(self):
        nodes = [
            TextNode("This is plain text without links.", TextType.PLAIN),
        ]

        result = split_nodes_link(nodes)

        expected = [
            TextNode("This is plain text without links.", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)
    
    def test_split_nodes_image(self):
        nodes = [
            TextNode("Here is an image: ![alt text](http://image.url) in text.", TextType.PLAIN),
        ]

        result = split_nodes_image(nodes)

        expected = [
            TextNode("Here is an image: ", TextType.PLAIN),
            TextNode("alt text", TextType.IMAGES, "http://image.url"),
            TextNode(" in text.", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)
    
    def test_no_images(self):
        nodes = [
            TextNode("This is plain text without images.", TextType.PLAIN),
        ]

        result = split_nodes_image(nodes)

        expected = [
            TextNode("This is plain text without images.", TextType.PLAIN),
        ]

        self.assertEqual(result, expected)

    def test_text_to_text_node(self):
        text = "This is **bold** and *italic* and `code`."
        result = text_to_text_node(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_text_to_text_node_no_formatting(self):
        text = "Just plain text."
        result = text_to_text_node(text)
        expected = [
            TextNode("Just plain text.", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_text_to_text_node_mixed(self):
        text = "**Bold** text with a [link](http://example.com) and an image ![alt](http://image.url)."
        result = text_to_text_node(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text with a ", TextType.PLAIN),
            TextNode("link", TextType.LINKS, "http://example.com"),
            TextNode(" and an image ", TextType.PLAIN),
            TextNode("alt", TextType.IMAGES, "http://image.url"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_text_to_text_node_empty(self):
        text = ""
        result = text_to_text_node(text)
        expected = []
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()