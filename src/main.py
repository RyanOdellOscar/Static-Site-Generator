from textnode import TextNode, TextType
import os
import shutil
from blocks import markdown_to_html_node
import sys
#In main.py use the sys.argv to grab the first CLI argument to the program. Save it as the basepath. If one isn't provided, default to /.
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
print('hello world')
#Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
#It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
#It should copy all files and subdirectories, nested files, etc.
#I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.
public_dir = "docs"

def delete_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def copy_contents(static, public):
    delete_contents(public)
    for item in os.listdir(static):
        item_path = os.path.join(static, item)
        dest_path = os.path.join(public, item)
        if os.path.isfile(item_path):
            shutil.copy2(item_path, dest_path)
        elif os.path.isdir(item_path):
            os.mkdir(dest_path)
            copy_contents(item_path, dest_path)
        else:
            raise Exception("unsupported file type")

def extract_title(markdown):
    if not "#" in markdown:
        raise Exception("no header found")
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line.lstrip("#").strip()
    raise Exception("no header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    md_html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page_html = (
        template.replace("{{title}}", title)
        .replace("{{ Title }}", title)
        .replace("{{Title}}", title)
        .replace("{{content}}", md_html)
        .replace("{{ Content }}", md_html)
        .replace("{{Content}}", md_html)
        .replace('href="/', 'href="{basepath}')
        .replace('src="/', 'src="{basepath}')
    )
        dest_dir = os.path.dirname(dest_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page_html)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
            if os.path.isfile(item_path):
                if item.endswith(".md"):
                    dest_path = os.path.splitext(dest_path)[0] + ".html"
                    generate_page(item_path, template_path, dest_path)
        elif os.path.isdir(item_path):
            os.mkdir(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path)
        else:
            raise Exception("unknown path")

def main():
    #after copying files from static to public, it should generate a page from content/index.md using template.html and write it to public/index.html
    #Run the generator to copy all the new stuff in static into the public directory.
    if not os.path.exists(public_dir):
        os.mkdir(public_dir)
    copy_contents("static", public_dir)
    generate_pages_recursive(basepath, "template.html", public_dir)


main()
