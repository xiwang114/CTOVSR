"""
Rename all frames of a video clip
"""

import os

# Input parent folder containing video clips
parent_folder = '/vol/data/abc/lq'

# Iterate over each subfolder in the parent folder
for subfolder_name in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, subfolder_name)
    if os.path.isdir(subfolder_path):
        # Get the list of files in the subfolder and sort them
        files = sorted(os.listdir(subfolder_path))
        for idx, file_name in enumerate(files):
            # Generate new file name
            new_file_name = f"{idx:08d}.png"
            old_file_path = os.path.join(subfolder_path, file_name)
            new_file_path = os.path.join(subfolder_path, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)

print("All frames have been renamed.")
