from textnode import TextNode
from htmlnode import HTMLNode
from copy_directory import copy_directory
from generation_tools import generate_page

def main():
    # copy static files first
    copy_directory('static', 'public')

    # generate pages for every markdown file under content/
    for dirpath, dirnames, filenames in __import__('os').walk('content'):
        for filename in filenames:
            if not filename.endswith('.md'):
                continue
            from_path = __import__('os').path.join(dirpath, filename)
            # compute destination path under public/ preserving structure
            rel = __import__('os').path.relpath(from_path, 'content')
            dest_rel = rel[:-3] + '.html'  # replace .md with .html
            dest_path = __import__('os').path.join('public', dest_rel)
            generate_page(
                from_path=from_path,
                template_path='template.html',
                dest_path=dest_path
            )

if __name__ == "__main__":
    main()