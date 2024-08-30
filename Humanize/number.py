import os

def rename_files_in_directory(directory):
    # Get all files in the directory
    files = os.listdir(directory)

    # Filter out non-mp3 files
    mp3_files = [f for f in files if f.endswith('.mp3')]

    # Create a list of tuples where the first element is the original filename
    # and the second element is the filename without the prefix
    mp3_files = [(filename, filename.split("_", 1)[1] if "_" in filename else filename) for filename in mp3_files]

    # Sort the files based on the filename without the prefix
    mp3_files.sort(key=lambda x: x[1])

    for i, (original_filename, filename) in enumerate(mp3_files, start=1):
        # Add the new number prefix
        new_name = f"{i}_{filename}"

        # Rename the file
        os.rename(os.path.join(directory, original_filename), os.path.join(directory, new_name))

# The current working directory is used
rename_files_in_directory('E:\\MASTER')