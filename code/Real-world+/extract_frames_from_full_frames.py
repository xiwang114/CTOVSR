"""
Extract frames from the sequence that has undergone the first step of spatial alignment to form video clips
"""

import os
import shutil

def extract_frame_segments(frames_dir, start_frame, interval, frame_count, total_segments):
    """
    Starting from the specified frame number, extract `frame_count` frames 
    every `interval` frames, and save them into multiple folders.
    Each folder contains images named from 00000000.png to 00000099.png.
    
    :param frames_dir: Directory containing all extracted frames
    :param start_frame: Starting frame number
    :param interval: Interval between segments (how many frames to skip each time)
    :param frame_count: Number of frames to extract per segment
    :param total_segments: Total number of segments to extract
    """
    folder_index = 0  # Folder index starts from 0

    # Get all frame files and sort them (assuming filenames are like '00143000-hd.png')
    frame_files = sorted(
        [f for f in os.listdir(frames_dir) if f.endswith('-hd.png')],
        key=lambda x: int(x.split('-')[0])  # Sort by the numeric frame ID
    )

    for segment in range(total_segments):
        # Calculate the start and end frame for each segment
        current_start_frame = start_frame + segment * interval
        current_end_frame = current_start_frame + frame_count

        # Create a folder to save this segment
        segment_folder = os.path.join('/vol/data/opera/gt', f'{folder_index:03d}')
        os.makedirs(segment_folder, exist_ok=True)

        # Copy the selected frames into the new folder and rename them sequentially
        image_name = 0
        for frame_file in frame_files[current_start_frame:current_end_frame]:
            src_path = os.path.join(frames_dir, frame_file)
            dst_path = os.path.join(segment_folder, f'{image_name:08d}.png')
            shutil.copy(src_path, dst_path)
            image_name += 1

        folder_index += 1
        print(f"Segment {folder_index}/{total_segments} extracted successfully")

# Example usage
if __name__ == '__main__':
    frames_directory = "/vol/data/final_full_frames"  # Replace with your actual frames folder path
    start_frame_number = 10000  # Start extracting from frame 10000
    frame_interval = 2000       # Extract every 2000 frames
    frames_per_segment = 100    # Extract 100 frames per segment
    total_segments = 50         # Extract 50 segments in total

    extract_frame_segments(frames_directory, start_frame_number, frame_interval, frames_per_segment, total_segments)
