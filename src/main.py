import sys
from functions.generate import copy_static, generate_pages_recursive

def main():
    # Get base path from CLI arg or default to "/"
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Use "docs" instead of "public"
    destination_dir = "docs"

    print(f"Generating site at base path: {base_path}")

    copy_static(destination=destination_dir)
    generate_pages_recursive("content", "template.html", destination_dir, base_path)

if __name__ == "__main__":
    main()
