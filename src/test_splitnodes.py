import unittest
from splitnodes import split_nodes_delimiter
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
            [
                TextNode("Hello", TextType.PLAIN),
                TextNode(",", TextType.PLAIN),
                TextNode(" ", TextType.PLAIN),
                TextNode("World", TextType.PLAIN),
                TextNode("!", TextType.PLAIN),
            ],
            [
                TextNode("\n", text_type)
            ],
            [
                TextNode("This", TextType.PLAIN),
                TextNode(" ", TextType.PLAIN),
                TextNode("is", TextType.PLAIN),
                TextNode(" ", TextType.PLAIN),
                TextNode("a", TextType.PLAIN),
                TextNode(" ", TextType.PLAIN),
                TextNode("test.", TextType.PLAIN),
            ]
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
            [
                TextNode("No", TextType.PLAIN),
                TextNode(" ", TextType.PLAIN),
                TextNode("delimiter", TextType.PLAIN),
            ]
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
            [
                TextNode("Line1", TextType.PLAIN),
            ],
            [
                TextNode("\n", text_type)
            ],
            [
                TextNode("\n", text_type)
            ],
            [
                TextNode("Line2", TextType.PLAIN),
            ]
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
            [
                TextNode("\n", text_type)
            ],
            [
                TextNode("Content", TextType.PLAIN),
            ],
            [
                TextNode("\n", text_type)
            ]
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
            [
                TextNode("\n", text_type)
            ],
            [
                TextNode("\n", text_type)
            ],
            [
                TextNode("\n", text_type)
            ]
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
            [
                TextNode("Just", TextType.PLAIN),
                TextNode("some", TextType.PLAIN),
                TextNode("text.", TextType.PLAIN),
            ]
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
            [
                TextNode("A", TextType.PLAIN),
                TextNode("B", TextType.PLAIN),
            ]
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
            [
                TextNode("This", TextType.PLAIN),
            ],
            [
                TextNode(" ", text_type)
            ],
            [
                TextNode("is", TextType.PLAIN),
            ],
            [
                TextNode(" ", text_type)
            ],
            [
                TextNode("bold", TextType.BOLD),
            ],
            [
                TextNode("!", TextType.PLAIN),
            ]
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
            [TextNode("*", text_type)],
            [TextNode("italic", TextType.PLAIN)],
            [TextNode("*", text_type)],
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
            [TextNode("This", TextType.PLAIN)],
            [TextNode("**", text_type)],
            [TextNode("bold", TextType.PLAIN)],
            [TextNode("**", text_type)],
            [TextNode("text", TextType.PLAIN)],
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
            [TextNode("`", text_type)],
            [TextNode("print('x')", TextType.PLAIN)],
            [TextNode("`", text_type)],
        ]

        self.assertEqual(result, expected)

    def test_link_delimiter(self):
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
            [TextNode("link", TextType.PLAIN)],
            [TextNode("[", text_type)],
            [TextNode("text", TextType.PLAIN)],
            [TextNode("]", TextType.PLAIN)],
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
            [TextNode("link", TextType.PLAIN)],
            [TextNode("[", text_type)],
            [TextNode("text", TextType.PLAIN)],
            [TextNode("]", TextType.PLAIN)],
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

        result = split_nodes_delimiter(nodes, delimiter, text_type)

        expected = [
            [TextNode("!", text_type)],
            [TextNode("[", TextType.PLAIN), TextNode("alt", TextType.PLAIN)],
            [TextNode("]", TextType.PLAIN)],
            [TextNode("(", TextType.PLAIN), TextNode("url", TextType.PLAIN), TextNode(")", TextType.PLAIN)],
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
            [TextNode("open", TextType.PLAIN), TextNode("*", TextType.BOLD), TextNode("close", TextType.PLAIN)]
        ]

        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()