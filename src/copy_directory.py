import os
import shutil

# A recursive function that copies all the contents from a source directory to a destination directory.
# first it deletes the contents of the destination directory if it exists.
# it should copy all files and subdirectories, nested files, etc. from source to destination.
# the path of each copied file should be logged to the console.
def copy_directory(source: str, destination: str):
    """
    Recursively copies a source directory to a destination directory,
    deleting the destination first if it exists, and logs copied file paths.
    """
    print(f"Starting copy from '{source}' to '{destination}'...")
    if os.path.exists(destination):
        print(f"Removing existing destination: {destination}")
        shutil.rmtree(destination)
        # shutil.copytree requires destination to not exist initially, so removing it works.
        # {Link: Python documentation https://docs.python.org/3/library/shutil.html}

    print(f"Copying '{source}' to '{destination}'...")
    shutil.copytree(source, destination) # This handles the recursive copy [1].

    print("Logging copied files:")
    # Walk through the newly copied destination to log files
    for dirpath, dirnames, filenames in os.walk(destination):
        for filename in filenames:
            print(os.path.join(dirpath, filename))

    print("Copy operation complete.")

# Example usage (replace with your actual paths):
# Assuming you have a 'my_source_folder' with files/subfolders
# and you want to copy them to 'my_destination_folder'
# copy_directory('path/to/source', 'path/to/destination')
