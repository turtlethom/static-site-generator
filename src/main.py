from functions.generate import copy_static, copy_dir_recursive, generate_page

def main():
    print("Copying static files...")
    copy_static("static", "public")
    print("Generating index.html...")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
