import sys
import os
import shutil
import glob

def get_dir_stats(directory):
    """
    Recursively calculates the total number of files and the total size of a directory.
    
    Args:
        directory (str): The path to the directory.
        
    Returns:
        tuple: A tuple containing (total_files, total_size_in_bytes).
    """
    total_files = 0
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        total_files += len(filenames)
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Ensure we don't follow symlinks to avoid errors and miscalculations
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                except OSError:
                    # File might be gone by the time we check, e.g. broken symlink
                    pass
    return total_files, total_size

def main():
    """
    Main function to parse arguments, read templates, and purge the directory.
    """
    # 1. Prompt for User Input
    folder_path = input("Enter the path to the folder you want to clean: ")

    python_file_dir = os.path.dirname(os.path.abspath(__file__))

    template_dir = os.path.join(python_file_dir, 'templates')
    templates = [f for f in os.listdir(template_dir) if f.endswith('.txt')]
    print("Available templates:")
    for t in templates:
        print(f" - {t[:-4]}")  # strip .txt extension

    template_name = input("Enter the template name to use (e.g., 'default'): ")
    template_path = os.path.join(python_file_dir, f'templates/{template_name}.txt')

    # 2. Validate Inputs
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' not found or is not a directory.")
        sys.exit(1)

    if not os.path.isfile(template_path):
        print(f"Error: Template file '{template_path}' not found.")
        sys.exit(1)

    print(f"\nStarting purge of '{folder_path}' using template '{template_name}'...")

    # 3. Get Initial Stats (Before Deletion)
    print("Calculating initial directory state...")
    initial_files, initial_size = get_dir_stats(folder_path)
    print(f"Before: {initial_files} files, {initial_size / (1024*1024):.2f} MB")
    print("-" * 40)

    # 4. Read Patterns and Find Items to Delete
    try:
        with open(template_path, 'r') as f:
            patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except IOError as e:
        print(f"Error reading template file: {e}")
        sys.exit(1)

    items_to_delete = set()
    for pattern in patterns:
        # Remove leading slash and use os.path.join for cross-platform compatibility
        clean_pattern = pattern.lstrip('/')
        # Create a glob pattern relative to the target folder
        glob_pattern = os.path.join(folder_path, clean_pattern)
        
        # The glob function understands standard wildcards:
        #   - '*' matches any characters except a path separator (e.g., 'Ax*' matches 'AxPets').
        #   - '?' matches a single character.
        #   - '**' can match any files and zero or more directories/subdirectories
        #     (this requires the `recursive=True` flag below).
        # Find all files and directories matching the pattern
        matches = glob.glob(glob_pattern, recursive=True)
        for match in matches:
            items_to_delete.add(os.path.abspath(match))

    # 5. Perform Deletion
    if not items_to_delete:
        print("No items found matching the template patterns. Nothing to do.")
    else:
        # Sort paths by length in descending order. This is a defensive measure
        # to handle nested items, e.g., deleting 'a/b/c' before 'a/b'.
        sorted_items = sorted(list(items_to_delete), key=len, reverse=True)

        for path in sorted_items:
            # Re-check existence, as a parent directory might have been deleted already
            if not os.path.exists(path) and not os.path.islink(path):
                continue

            try:
                if os.path.isfile(path) or os.path.islink(path):
                    os.remove(path)
                    print(f"[PURGED FILE] {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"[PURGED DIR]  {path}")
            except Exception as e:
                print(f"Could not delete {path}. Reason: {e}")

    print("-" * 40)
    print("Purge complete. Calculating final stats...")

    # 6. Get Final Stats and Calculate Differences
    final_files, final_size = get_dir_stats(folder_path)
    
    deleted_files_count = initial_files - final_files
    space_saved_bytes = initial_size - final_size
    space_saved_mb = space_saved_bytes / (1024 * 1024)

    # Avoid division by zero errors
    percent_files_deleted = (deleted_files_count / initial_files * 100) if initial_files > 0 else 0
    percent_space_saved = (space_saved_bytes / initial_size * 100) if initial_size > 0 else 0

    # Format original and final sizes for display
    initial_size_mb = initial_size / (1024 * 1024)
    final_size_mb = final_size / (1024 * 1024)

    print("\n--- Purge Summary ---")
    print(f"Total Files: {initial_files} -> {final_files} ({percent_files_deleted:.2f}% deleted)")
    print(f"Total Storage Space: {initial_size_mb:.2f} MB -> {final_size_mb:.2f} MB ({percent_space_saved:.2f}% saved)")
    print("---------------------")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        input("\nPress Enter to close the window...")

