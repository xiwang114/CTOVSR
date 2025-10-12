"""
Resize the frames of each video clip in the source folder
"""

import os
import argparse
import numpy as np
from PIL import Image, ImageFile
from scipy import interpolate

ImageFile.LOAD_TRUNCATED_IMAGES = True

def catmull_rom_resample(image, new_size):
    old_size = image.size
    x_old = np.linspace(0, old_size[0] - 1, old_size[0])
    y_old = np.linspace(0, old_size[1] - 1, old_size[1])
    
    x_new = np.linspace(0, old_size[0] - 1, new_size[0])
    y_new = np.linspace(0, old_size[1] - 1, new_size[1])
    
    interpolated = interpolate.interp2d(x_old, y_old, np.array(image), kind='cubic')
    return Image.fromarray(interpolated(x_new, y_new).astype(np.uint8))

def resize_images_in_subfolders(source_directory, target_directory, width=480, height=270, method='lanczos'):
    skipped_files = []

    try:
        subfolders = [d for d in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, d))]
        
        for subfolder in subfolders:
            source_subfolder_path = os.path.join(source_directory, subfolder)
            target_subfolder_path = os.path.join(target_directory, subfolder)

            if not os.path.exists(target_subfolder_path):
                os.makedirs(target_subfolder_path)

            files = [f for f in os.listdir(source_subfolder_path) if f.endswith('.png')]

            for filename in files:
                source_file_path = os.path.join(source_subfolder_path, filename)
                target_file_path = os.path.join(target_subfolder_path, filename)

                if os.path.exists(target_file_path):
                    skipped_files.append(os.path.join(subfolder, filename))
                    print(f"Skipped (already exists): {os.path.join(subfolder, filename)}")
                    continue

                with Image.open(source_file_path) as img:
                    if method == 'catmullrom':
                        img_resized = catmull_rom_resample(img, (width, height))
                    else:
                        resample_method = {
                            'bicubic': Image.BICUBIC,
                            'bilinear': Image.BILINEAR,
                            'lanczos': Image.LANCZOS
                        }.get(method, Image.LANCZOS)
                        img_resized = img.resize((width, height), resample_method)

                    img_resized.save(target_file_path)
                    print(f"Resized and saved: {os.path.join(subfolder, filename)}")

        print(f'\nResize completed. Skipped {len(skipped_files)} files that already existed.')
        if skipped_files:
            print("List of skipped files:")
            for file in skipped_files:
                print(f"  - {file}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resize images in subfolders.')
    parser.add_argument('--method', type=str, choices=['catmullrom', 'bicubic', 'bilinear', 'lanczos'], default='lanczos', help='Resampling method to use.')
    args = parser.parse_args()

    source_directory_path = '/vol/data/gt'
    target_directory_path = '/vol/data/target'

    resize_images_in_subfolders(source_directory_path, target_directory_path, width=1920, height=1080, method=args.method)