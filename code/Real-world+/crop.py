"""
Crop the temporally aligned sequence to remove watermarks and black borders
This also constitutes the first step of spatial alignment
"""

from PIL import Image
import os

# Set input and output folder paths, and crop parameters
input_folder = '/vol/data/full_frames'
output_folder = '/vol/data/final_full_frames'

# Manually determined crop box: (left, upper, right, lower)
crop_box = (71, 55, 71 + 490, 55 + 276)

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through all images in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.png'):  # Add other formats if needed
        image_path = os.path.join(input_folder, filename)
        img = Image.open(image_path)
        
        # Crop the image
        cropped_img = img.crop(crop_box)
        
        # Save the cropped image to the output folder
        cropped_img.save(os.path.join(output_folder, filename))

print("Cropping completed!")
