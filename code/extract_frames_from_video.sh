#!/bin/bash

# List of input video files
input_videos=(
)

# List of output folders
output_folders=()

# Construct output folder list (from 000 to 099)
for i in {0..99}
do
    output_folders+=("/vol/data/gt/$(printf "%03d" $i)")
done

# List of time segments (start_time-end_time, format HH:MM:SS)
# Each video has multiple segments
time_segments=("00:10:00-00:10:05")

# Frame rate for extraction (frames per second)
frame_rate=N

# Iterate over each input video
for i in "${!input_videos[@]}"
do
    input_video="${input_videos[$i]}"
    
    # Process each time segment and corresponding output folder
    for index in "${!time_segments[@]}"
    do
        # Extract start time and end time
        start_time=$(echo "${time_segments[$index]}" | cut -d'-' -f1)
        end_time=$(echo "${time_segments[$index]}" | cut -d'-' -f2)
        
        # Create the output folder if it doesn't exist
        output_folder="${output_folders[$((i * 5 + index))]}"
        mkdir -p "$output_folder"
        
        # Use ffmpeg to extract frames and save them in the output folder
        ffmpeg -i "$input_video" -r "$frame_rate" -ss "$start_time" -to "$end_time" "$output_folder/%08d.png"
    done
done

echo "Frame extraction completed."
