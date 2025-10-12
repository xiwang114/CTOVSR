"""
Rename all video clips in the folder
"""

import os

# Parent folder containing the video clips
parent_folder = '/vol/data/gt'  # Replace with the actual parent folder path

# Get all subfolders
subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

# Sort the subfolders
subfolders.sort()

# Iterate over subfolders and rename them
for index, old_folder_name in enumerate(subfolders):
    old_folder_path = os.path.join(parent_folder, old_folder_name)
    new_folder_name = f"{index:03d}"
    new_folder_path = os.path.join(parent_folder, new_folder_name)
        
    # Rename the folder
    os.rename(old_folder_path, new_folder_path)

print("All video clips have been renamed.")
