import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown(self):
        text  = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item"
        self.assertListEqual(markdown_to_blocks(text), [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item']
        )

    def test_markdown_trailingspace(self):
        text  = "   # This is a heading\n\n  This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n  * This is the first list item in a list block\n* This is a list item"
        self.assertListEqual(markdown_to_blocks(text), [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item']
        )

    def test_markdown_emptyblocks(self):
        text  = "# This is a heading\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n* This is the first list item in a list block\n* This is a list item"
        self.assertListEqual(markdown_to_blocks(text), [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item']
        )
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING.value)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE.value)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE.value)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST.value)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST.value)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH.value)

if __name__ == "__main__":
    unittest.main()