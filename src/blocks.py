from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    new_blocks = []
    current_block = ""
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.strip() == "":
            continue
        new_blocks.append(block.strip())

    return new_blocks

def block_to_block_type(block):
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    if (block.startswith("```\n") and block.endswith("\n```")) or (block.startswith("```") and block.endswith("```")):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if block.startswith("- ") or block.startswith("* "):
        return BlockType.ULIST
    if block.startswith("1. "):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                heading_level = 0
                while block.startswith("#"):
                    heading_level += 1
                    block = block[1:]
                children.append(ParentNode(f"h{heading_level}", [text_node_to_html_node(text) for text in text_to_textnodes(block.strip())]))
            case BlockType.CODE:
                code_content = block[4:-3]
                raw_text_node = TextNode(code_content, TextType.TEXT)
                children.append(ParentNode("pre", [ParentNode("code", [text_node_to_html_node(raw_text_node)])]))
            case BlockType.QUOTE:
                quote_lines = [line[2:].strip() for line in block.split("\n") if line.strip()]
                quote_text = " ".join(quote_lines)
                children.append(ParentNode("blockquote", [text_node_to_html_node(text) for text in text_to_textnodes(quote_text)]))
            case BlockType.ULIST:
                items = [item.strip()[2:].strip() for item in block.split("\n") if item.strip()]
                children.append(ParentNode("ul", [ParentNode("li", [text_node_to_html_node(text) for text in text_to_textnodes(item)]) for item in items]))
            case BlockType.OLIST:
                items = [item.strip()[3:].strip() for item in block.split("\n") if item.strip()]
                children.append(ParentNode("ol", [ParentNode("li", [text_node_to_html_node(text) for text in text_to_textnodes(item)]) for item in items]))
            case BlockType.PARAGRAPH:
                paragraph = " ".join(line.strip() for line in block.split("\n") if line.strip())
                children.append(ParentNode("p", [text_node_to_html_node(text) for text in text_to_textnodes(paragraph)]))
    return ParentNode("div", children, None)