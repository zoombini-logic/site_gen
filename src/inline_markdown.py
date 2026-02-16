from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if (node.text.count(delimiter) == 0):
                new_nodes.append(node)
                continue 
            if(node.text.count(delimiter) % 2 != 0):
                raise Exception ("invalid number of delimiters in node")
            split_node = node.text.split(delimiter)
            #print(f'Split Node: {split_node}')

            node_split_count = 1
            for node_text in split_node:
                if (node_split_count % 2 == 0):
                    new_nodes.append(TextNode(node_text, text_type))
                elif len(node_text)> 0:
                    new_nodes.append(TextNode(node_text, TextType.TEXT))
                node_split_count += 1
    return new_nodes

def extract_markdown_images(text):
    return_list = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return return_list

def extract_markdown_links(text):
    return_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return return_list

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        content = node.text
        link_list = extract_markdown_links(content)
        if link_list == []:
            new_nodes.append(node)
            continue      
        for link in link_list:
            link_text = link[0]
            link_address = link[1]
            sections = content.split(f"[{link_text}]({link_address})",1)
            if (sections[0] != ''):
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_address))
            content = sections[1]
        if (content != ''):
            new_nodes.append(TextNode(content, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
     new_nodes = []
     for node in old_nodes:
        content = node.text
        link_list = extract_markdown_images(content)
        if link_list == []:
            new_nodes.append(node)
            continue                 
        for link in link_list:
            image_text = link[0]
            image_address = link[1]
            sections = content.split(f"![{image_text}]({image_address})",1)
            if (sections[0] != ''):
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_address))
            content = sections[1]
        if (content != ''):
            new_nodes.append(TextNode(content, TextType.TEXT))
     return new_nodes
   
def text_to_textnodes(text):
    temp_node = TextNode(text, TextType.TEXT)
    return_nodes = split_nodes_delimiter([temp_node], "**", TextType.BOLD)
    return_nodes = split_nodes_delimiter(return_nodes, "_", TextType.ITALIC)
    return_nodes = split_nodes_delimiter(return_nodes, "`", TextType.CODE)
    return_nodes = split_nodes_image(return_nodes)
    return_nodes = split_nodes_link(return_nodes)
    return return_nodes


def markdown_to_blocks(markdown):
    return_list = []
    block_list = markdown.split('\n\n')
    for block in block_list:
        return_list.append(block.strip('\n'))
    return return_list