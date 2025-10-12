import os
import cv2
from degrade import degrade_img

# Path to your high resolution video clip
main_path = "/vol/data/gt"

# Path to save degraded video clip
save_path = "/vol/data/lq"

def process_all_images():
    for folder in os.listdir(main_path):
        folder_path = os.path.join(main_path, folder)
        if os.path.isdir(folder_path):
            for img_file in os.listdir(folder_path):
                if img_file.endswith(".png"): 
                    img_path = os.path.join(folder_path, img_file)
                    src = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

                    # Apply degradation to the image
                    frame = degrade_img(src)
                    resize_dim = (320, 180)
                    src = cv2.resize(src, resize_dim, interpolation=cv2.INTER_AREA)
                    frame = 255 * frame

                    # Save the degraded image
                    save_loc = os.path.join(save_path, folder)
                    os.makedirs(save_loc, exist_ok=True)  # Create folder if it doesn't exist
                    save_path_full = os.path.join(save_loc, img_file)
                    cv2.imwrite(save_path_full, frame)

                    print(f"Degraded frame saved: {save_path_full}")

def main():
    process_all_images()

if __name__ == "__main__":
    main()
