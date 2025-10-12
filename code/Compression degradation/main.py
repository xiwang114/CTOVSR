"""
Compress high-definition videos to generate low-resolution videos
"""

import subprocess
import os

# List of input videos
input_videos = [
    # Add the rest of the video paths
]

# Output directory
output_dir = "/vol/data/video"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over the list of videos
for video in input_videos:
    # Get the video file name without extension
    video_name = os.path.splitext(os.path.basename(video))[0]
    
    # Set the output file path
    output_file = os.path.join(output_dir, f"{video_name}.mp4")
    
    # Construct the ffmpeg command
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video,                          # Input video
        "-vf", "scale=in_range=full:out_range=limited",  # Use video filter to set color range
        "-s", "480x270",                      # Set resolution
        "-c:v", "libx264",                    # Use x264 encoder (H.264)
        "-crf", "25",                         # Set CRF (quality control)
        "-preset", "superfast",               # Set encoding speed
        output_file                            # Output file path
    ]
    
    # Execute the ffmpeg command
    try:
        print(f"Processing: {video}")
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Completed: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {video}: {e}")
