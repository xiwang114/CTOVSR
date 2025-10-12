"""
Compute the average SSIM for each HD segment and its corresponding low-resolution segment; 
segments with an average SSIM below 0.95 will be deleted
"""


import os
import logging
from PIL import Image
import numpy as np

# Configure logging
logging.basicConfig(
    filename="delete.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def compute_img_ssim(img1, img2):
    """
    Compute SSIM between two grayscale images
    """
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    img1 = np.array(img1, dtype=np.float64)
    img2 = np.array(img2, dtype=np.float64)

    mu_x = np.mean(img1)
    mu_y = np.mean(img2)
    sigma_x = np.var(img1)
    sigma_y = np.var(img2)
    sigma_xy = np.mean((img1 - mu_x) * (img2 - mu_y))

    numerator = (2 * mu_x * mu_y + c1) * (2 * sigma_xy + c2)
    denominator = (mu_x ** 2 + mu_y ** 2 + c1) * (sigma_x + sigma_y + c2)

    return numerator / denominator

def compute_lanczos_ssim_per_segment(hd_dir, fd_dir, threshold=0.95):
    """
    Compute the average SSIM for each segment between HD and low-resolution
    frames resized with Lanczos interpolation.
    If the average SSIM is below the threshold, log and print a warning.
    """
    for segment in os.listdir(hd_dir):
        hd_segment_path = os.path.join(hd_dir, segment)
        fd_segment_path = os.path.join(fd_dir, segment)

        if not os.path.isdir(hd_segment_path) or not os.path.isdir(fd_segment_path):
            continue

        ssim_values = []  # Store SSIM values for each frame in the segment

        for frame in os.listdir(hd_segment_path):
            hd_frame_path = os.path.join(hd_segment_path, frame)
            fd_frame_path = os.path.join(fd_segment_path, frame)

            if not os.path.isfile(hd_frame_path) or not os.path.isfile(fd_frame_path):
                continue

            hd_img = Image.open(hd_frame_path).convert('L')
            fd_img = Image.open(fd_frame_path).convert('L')
            
            # The interpolation method used has no effect
            # Resize low-res image to HD size using Lanczos interpolation
            fd_img_lanczos = fd_img.resize(hd_img.size, Image.Resampling.LANCZOS)
            #fd_img_lanczos = fd_img.resize(hd_img.size, Image.Resampling.BICUBIC)
            ssim_value = compute_img_ssim(hd_img, fd_img_lanczos)
            ssim_values.append(ssim_value)

        # Compute average SSIM for the segment
        if ssim_values:
            avg_ssim = np.mean(ssim_values)
            if avg_ssim < threshold:
                message = f"Segment '{segment}' average SSIM below threshold {threshold}, average SSIM: {avg_ssim:.4f}"
                print(message)
                logging.info(message)
            else:
                message = f"Segment '{segment}' checked, average SSIM: {avg_ssim:.4f}"
                print(message)
                logging.info(message)

# Example usage
hd_dir = "/vol/data/opera/gt"
fd_dir = "/vol/data/opera/lq"
compute_lanczos_ssim_per_segment(hd_dir, fd_dir)
