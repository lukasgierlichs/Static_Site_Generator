import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_paragraphs(self):
        md = "Para one.\n\nPara two."
        self.assertEqual(markdown_to_blocks(md), ["Para one.", "Para two."])

    def test_multiple_blank_lines(self):
        md = "A\n\n\nB"
        self.assertEqual(markdown_to_blocks(md), ["A", "B"])

    def test_leading_trailing_whitespace(self):
        md = "  A  \n\n B "
        self.assertEqual(markdown_to_blocks(md), ["A", "B"])
    
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        # Inline single-line fenced code (```code```) is treated as a paragraph
        # in this simplified implementation.
        self.assertEqual(block_to_block_type("```code block```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. First\n2. Second"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
    
    def test_ordered_list_within_limits(self):
        md = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth\n6. Sixth\n7. Seventh\n8. Eighth\n9. Ninth\n10. Tenth"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)
    
    def test_ordered_list_exceeding_limits(self):
        md = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth\n6. Sixth\n7. Seventh\n8. Eighth\n9. Ninth\n10. Tenth\n11. Eleventh"
        # With no artificial upper limit, this should still be recognized
        # as an ordered list if the numbering is sequential starting from 1.
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)
    
    def test_mixed_ordered_list(self):
        md = "1. First\n2. Second\nThree. Third"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_quote_multiline(self):
        md = "> This is a quote\n> that spans multiple lines."
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)
    
    def test_non_quote_multiline(self):
        md = "> This is a quote\nThis is not a quote."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_non_unordered_list_multiline(self):
        md = "- Item 1\nItem 2"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_non_heading(self):
        md = "####### Not a heading"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_code_block_not_ending(self):
        md = "```This is a code block without an ending"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_code_block_not_starting(self):
        md = "This is a code block without a starting```"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_code_block_proper(self):
        md = "```\nThis is a proper code block\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)
    
    def test_heading_with_leading_whitespace(self):
        md = "   ### Heading with spaces"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)
    
    def test_unordered_list_with_leading_whitespace(self):
        md = "   - Item 1\n   - Item 2"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)
    
    def test_ordered_list_with_leading_whitespace(self):
        md = "   1. First\n   2. Second"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)
    
    def test_quote_with_leading_whitespace(self):
        md = "   > This is a quote"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)
    
    def test_paragraph_with_leading_whitespace(self):
        md = "   This is a paragraph."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_empty_block(self):
        md = ""
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_whitespace_only_block(self):
        md = "     "
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_single_line_code_block(self):
        md = "```inline code```"
        # Inline fenced code is not treated as a code block in the simplified
        # assignment; it is considered a paragraph here.
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_heading_with_trailing_text(self):
        md = "### Heading ###"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)
    
    def test_unordered_list_with_mixed_indentation(self):
        md = "- Item 1\n   - Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)
    
    def test_non_quote_multiline_paragraph(self):
        md = "> This is a quote\nThis is not a quote.\n> Another quote line."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
