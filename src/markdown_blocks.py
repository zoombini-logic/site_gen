from enum import Enum
import re
from htmlnode import *
from textnode import *
from inline_markdown import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return_list = []
    block_list = markdown.split('\n\n')
    for block in block_list:
        if block != '':
            return_list.append(block.strip('\n'))
    return return_list

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    child_node_list = []
    for block in blocks:
        match (block_to_block_type(block)):
            case BlockType.PARAGRAPH:
                new_block = block.replace("\n"," ")
                html_block = ParentNode("p", text_to_children(new_block))
            case BlockType.HEADING:
                h_num = block.index(" ")
                #print(f"\nLeaf Node value = {block[h_num + 1:]}")
                html_block = ParentNode(f"h{h_num}", text_to_children(block[h_num+1:]))
            case BlockType.CODE:
                new_code = block.replace("\n", "\\n")
                code_node = TextNode(block[4:-3], TextType.CODE)
 #               print(f'\nCode Node: {code_node}')
                code_node_list = []
                code_node_list.append(text_node_to_html_node(code_node))
                html_block = ParentNode("pre", code_node_list)
#                print(f'\nCode block: {html_block}')
            case BlockType.QUOTE:
                edited_quote = ""
                lines = block.split("\n")
                for line in lines:
                    if (len(line) > 1) and (line[1] == " "):
                        line_index = 2
                    else:
                        line_index = 1
                    edited_quote = edited_quote + line[line_index:] + " "
                html_block = ParentNode("blockquote", text_to_children(edited_quote[:-1]))
            case BlockType.UNORDERED_LIST:
                lines_list = []
                lines = block.split("\n")
                for line in lines:
                    line_node = ParentNode("li", text_to_children(line[2:]))
                    lines_list.append(line_node)
                html_block = ParentNode("ul", lines_list)
            case BlockType.ORDERED_LIST:
                lines_list = []
                lines = block.split("\n")
                for line in lines:
                    line_node = ParentNode("li", text_to_children(line[3:]))
                    lines_list.append(line_node)
                html_block = ParentNode("ol", lines_list)
        child_node_list.append(html_block)
   
    html_parent = ParentNode("div", child_node_list)
    return html_parent


            

def text_to_children(text):
    return_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        return_nodes.append(text_node_to_html_node(node))
    return return_nodes

#this expects a string
def extract_title(markdown):
    start_block = markdown_to_blocks(markdown)[0]
    lines = start_block.split("\n")
    if not (lines[0].startswith("# ")):
        raise Exception ("Markdown file doesn't start with a header line")
    return lines[0][2:]
