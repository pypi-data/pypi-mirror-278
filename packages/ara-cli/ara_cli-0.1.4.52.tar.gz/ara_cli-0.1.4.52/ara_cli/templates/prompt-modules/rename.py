import os

def rename_files(directory):
    # Walk through all directories and files in the provided directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file starts with 'template_' and ends with '.md'
            if file.startswith("template_") and file.endswith(".md"):
                old_file_path = os.path.join(root, file)
                # Generate the new file name by stripping 'template_' prefix
                new_file_name = file.replace("template_", "")
                new_file_path = os.path.join(root, new_file_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed '{old_file_path}' to '{new_file_path}'")

# Specify the directory to start from
start_directory = "."
rename_files(start_directory)
