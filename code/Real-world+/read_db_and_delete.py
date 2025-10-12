"""
First, use ffmpeg to extract all frames from the entire video
Then, use the following code to delete frames based on the database exported by **eye_compare tool**
This step performs temporal alignment
"""

import sqlite3
import os
import re

# Increment numeric parts in file names by 1
def increment_numbers(file_names):
    updated_file_names = []
    for file_name in file_names:
        # Use regex to extract the numeric part
        match = re.search(r'(\d+)', file_name)
        if match:
            # Increment the numeric part by 1
            number = int(match.group(0)) + 1
            # Format the number to 7 digits and replace the original numeric part
            new_file_name = re.sub(r'\d+', f'{number:07d}', file_name, 1)
            updated_file_names.append(new_file_name)
    return updated_file_names

# Connect to the SQLite database (.db file)
db_file = '/vol/data/qinbingxin/database/opera.db'  # Replace with your database file path
conn = sqlite3.connect(db_file)

# Create a cursor object
cursor = conn.cursor()

# Query all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

deleted_paths = []
file_names = []

# Iterate over each table and read data
for table in tables:
    table_name = table[0]
    
    if table_name == 'dir_images':
        print(f"Table: {table_name}")
        
        # Query 'path' column where deleted = 1
        cursor.execute(f"SELECT path FROM {table_name} WHERE deleted = 1;")
        rows = cursor.fetchall()

        # Extract path column
        deleted_paths = [row[0] for row in rows]
        for deleted_path in deleted_paths:
            unix_style_path = deleted_path.replace('\\', '/')
            file_name = os.path.basename(unix_style_path)  # Extract file name
            file_name = file_name.replace(".jpg", ".png")
            file_names.append(file_name)  # Add to list

# Increment numeric parts in filenames
updated_file_names = increment_numbers(file_names)

# Close cursor and connection
cursor.close()
conn.close()

# Iterate through updated file names, build full path, and delete files
for file_name in updated_file_names:
    # Build full file path
    full_path = os.path.join("/vol/data/full_frames", file_name)
    print(full_path)
    
    try:
        # Delete the file
        os.remove(full_path)
        print(f"Deleted file: {full_path}")
    except FileNotFoundError:
        print(f"File not found: {full_path}")
    except PermissionError:
        print(f"No permission to delete file: {full_path}")
    except Exception as e:
        print(f"Error deleting file: {full_path}, Error: {e}")
