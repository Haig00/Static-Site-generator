import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

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

    def test_markdown_to_html(self):
        text  = "## This **is a** heading"
        self.assertEqual(markdown_to_html_node(text).__repr__(),
         "ParentNode(div, children: [ParentNode(h2, children: [LeafNode(None, This , None), LeafNode(b, is a, None), LeafNode(None,  heading, None)], None)], None)")

        self.assertEqual(markdown_to_html_node(text).to_html(), 
            "<div><h2>This <b>is a</b> heading</h2></div>")
        
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()