from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import *
from markdown_blocks import *
import os
import shutil
import sys


def main():
    if (len(sys.argv)> 1):
        basepath = sys.argv[1]
    else:
        basepath = '/'
    print(basepath)
    copy_over_dir("./static", "./docs")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

def copy_over_dir(source, destination):
    if (os.path.exists(source) == False):
        raise Exception ("Source does not exist")
    if (os.path.exists(destination)):
        shutil.rmtree(destination)
        print(f"removed {destination}")
    else:
        print(f"{destination} does not exist, so no deletion occurred")
    os.mkdir(destination)
    #print(f"created {destination}")
    source_entities = os.listdir(source)
    #print (source_entities)
    for dir_object in source_entities:
        object_path = source + "/" + dir_object
        dest_path = destination + "/" + dir_object
        if os.path.isfile(object_path):
            shutil.copy(object_path, dest_path)
            #print(f"copied {object_path} to {dest_path}")
        else:
            copy_over_dir(object_path, dest_path)
        
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, 'r')
    from_string = from_file.read()
    from_file.close()
    template_file = open(template_path, 'r')
    template_string = template_file.read()
    template_file.close()
    from_html_string = markdown_to_html_node(from_string).to_html()
    #print (from_html_string)
    title = extract_title(from_string)
    to_html_string = template_string.replace("{{ Title }}", title)
    to_html_string = to_html_string.replace("{{ Content }}", from_html_string)
    to_html_string = to_html_string.replace('href="/', f'href="{basepath}')
    to_html_string = to_html_string.replace('src="/', f'src="{basepath}')
    #print (to_html_string)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    dest_file = open(dest_path, 'w')
    dest_file.write(to_html_string)
    dest_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    object_list = os.listdir(dir_path_content)
    for object in (object_list):
        object_path = dir_path_content + "/" + object
        if (os.path.isfile(object_path) and object[-3:] == ".md"):
            dest_file_name = dest_dir_path + "/" + object.replace(".md", ".html")
            generate_page(object_path, template_path, dest_file_name, basepath)
        if not (os.path.isfile(object_path)):
            new_dest_dir_path = dest_dir_path + "/" + object
            generate_pages_recursive(object_path, template_path, new_dest_dir_path, basepath)




main()