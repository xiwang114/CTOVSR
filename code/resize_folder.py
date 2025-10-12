"""
Resize all frames of the current video clip
"""

import os
from PIL import Image

# Root folder containing the frames
root_dir = '/vol/data/gt/000'
# Target folder to save resized images
output_dir = '/vol/data/target/000'

# Desired size
new_size = (512, 512)

# Make sure the target folder exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over all images in the root folder
for file_name in os.listdir(root_dir):
    file_path = os.path.join(root_dir, file_name)
    if os.path.isfile(file_path) and file_name.lower().endswith(('png', 'jpg', 'jpeg')):
        # Open the image and resize
        with Image.open(file_path) as img:
            img_resized = img.resize(new_size)

            # Construct the output file path
            output_file_path = os.path.join(output_dir, file_name)
            img_resized.save(output_file_path)  # Save to the target folder
        print(f"Resized and saved: {output_file_path}")

print("All frames processed!")
