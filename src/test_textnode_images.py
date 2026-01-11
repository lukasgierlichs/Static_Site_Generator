import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNodeImages(unittest.TestCase):
    def test_images(self):
        node = TextNode("Alt text", TextType.IMAGES, url="http://img.example/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://img.example/img.png", "alt": "Alt text"})

    def test_images_no_url_raises(self):
        node = TextNode("Alt text", TextType.IMAGES)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
