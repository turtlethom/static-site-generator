import os
from pathlib import Path
from .nodehelpers import markdown_to_html_node
from .extracters import extract_title

def copy_static(source="static", destination="public"):
    # Step 1: Remove destination directory manually if it exists
    if os.path.exists(destination):
        print(f"Removing existing directory: {destination}")
        remove_dir_recursive(destination)

    # Step 2: Create the destination directory
    os.makedirs(destination)

    # Step 3: Recursively copy from source to destination
    copy_dir_recursive(source, destination)

def remove_dir_recursive(path):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            remove_dir_recursive(full_path)
        else:
            print(f"Deleting file: {full_path}")
            os.remove(full_path)
    print(f"Removing directory: {path}")
    os.rmdir(path)

def copy_dir_recursive(src, dst):
    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)

        if os.path.isdir(src_path):
            os.makedirs(dst_path)
            copy_dir_recursive(src_path, dst_path)
        else:
            with open(src_path, "rb") as f_src:
                content = f_src.read()
            with open(dst_path, "wb") as f_dst:
                f_dst.write(content)
            print(f"Copied: {src_path} → {dst_path}")

def generate_page(from_path, template_path, dest_path, base_path="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read markdown content
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    # Read template content
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    # Replace placeholders
    full_html = (
        template_content
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
        .replace('href="/', f'href="{base_path}')
        .replace('src="/', f'src="{base_path}')
    )
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # Write the final HTML to the destination path
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                # Build full path to the markdown file
                md_path = os.path.join(root, file)
                
                # Build corresponding destination path
                rel_path = os.path.relpath(md_path, dir_path_content)  # e.g., "blog/post.md"
                dest_rel_path = os.path.splitext(rel_path)[0] + ".html"  # replace .md with .html
                dest_path = os.path.join(dest_dir_path, dest_rel_path)

                # Ensure destination directory exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                print(f"Generating {md_path} -> {dest_path}")
                generate_page(md_path, template_path, dest_path, base_path)
