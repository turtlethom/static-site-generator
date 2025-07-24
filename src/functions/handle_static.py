import os

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
