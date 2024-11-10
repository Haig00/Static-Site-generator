from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from split_node import text_to_text_nodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    fixed = []
 
    for blocks in split_markdown:
        if blocks != "":
            fixed.append(blocks.strip())
    return fixed


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING.value
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE.value
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH.value
        return BlockType.QUOTE.value
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED_LIST.value
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED_LIST.value
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH.value
            i += 1
        return BlockType.ORDERED_LIST.value
    return BlockType.PARAGRAPH.value

def heading_fixer(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_fixer(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    
    code_no_markdown = block[4:-4]
    code_block = ParentNode("code", text_to_children(code_no_markdown))
    return ParentNode("pre", [code_block], None)

def quote_fixer(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children, None)

def unordered_list_fixer(ul):
    new_ul = ul.split("\n")
    nodes_ul = []
    for line in new_ul:
        unordered_list_no_markdown = line[2:]
        
        nodes_ul.append(ParentNode("li", text_to_children(unordered_list_no_markdown), None))
    return ParentNode("ul", nodes_ul, None)

def ordered_list_fixer(ol):
    new_ol = ol.split("\n")
    nodes_ol = []
    count = 1
    for line in new_ol:
        ordered_list_no_markdown = line.replace(f"{count}. ", "", 1)
        nodes_ol.append(ParentNode("li", text_to_children(ordered_list_no_markdown), None))
        count += 1
    return ParentNode("ol", nodes_ol, None)

def paragraph_fixer(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def text_to_children(text):
    return children_to_leaf(text_to_text_nodes(text))

def children_to_leaf(nodes):
    leafs  = []
    for node in nodes:
        leafs.append(text_node_to_html_node(node))
    
    return leafs

def markdown_to_html_node(markdown):
    block_markdown = markdown_to_blocks(markdown)
    list_of_nodes = []
    #print(block_markdown)
    for block in block_markdown:
     
        if block_to_block_type(block) == "heading":
            list_of_nodes.append((heading_fixer(block)))
        if block_to_block_type(block) == "code":
            list_of_nodes.append(code_fixer(block))
        if block_to_block_type(block) == "quote":
            list_of_nodes.append(quote_fixer(block))
        if block_to_block_type(block) == "unordered_list":
            list_of_nodes.append(unordered_list_fixer(block))
        if block_to_block_type(block) == "ordered_list":
            list_of_nodes.append(ordered_list_fixer(block))
        if block_to_block_type(block) == "paragraph":
            list_of_nodes.append(paragraph_fixer(block))
    #print(list_of_nodes)
    return ParentNode("div", list_of_nodes, None)

            
if __name__ == "__main__":
    text  = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
    print(markdown_to_blocks(text))
    print(markdown_to_html_node(text).__repr__())
    print(markdown_to_html_node(text).to_html())
    
