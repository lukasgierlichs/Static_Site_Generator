import unittest
from markdown_extractor import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Here is an image: ![Alt text](http://example.com/image.png) in the text."
        expected = [("Alt text", "http://example.com/image.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_multiple_markdown_images(self):
        text = "Images: ![Img1](http://example.com/img1.png) and ![Img2](http://example.com/img2.jpg)."
        expected = [("Img1", "http://example.com/img1.png"), ("Img2", "http://example.com/img2.jpg")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "Here is a link: [Link text](http://example.com) in the text."
        expected = [("Link text", "http://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_multiple_markdown_links(self):
        text = "Links: [Link1](http://example.com/1) and [Link2](http://example.com/2)."
        expected = [("Link1", "http://example.com/1"), ("Link2", "http://example.com/2")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_no_images(self):
        text = "This text has no images."
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_no_links(self):
        text = "This text has no links."
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
    
if __name__ == "__main__":
    unittest.main()