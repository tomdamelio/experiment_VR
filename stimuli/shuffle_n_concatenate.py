#%%

import moviepy.editor as mp
import random
import os
import pandas as pd


def resize_clip(clip, target_resolution):
    return clip.resize(target_resolution)

def process_videos_and_image(video_paths, output_resolution, order_matrix):
    # Shuffle the videos in a pseudo-random order (all videos selected exactly once)
    random.shuffle(video_paths)
    print(f'Orden: {video_paths}')
    # Add video files, block numbers, and video ids to the order matrix
    order_matrix = pd.concat([order_matrix, pd.DataFrame({'video_files': video_paths})], axis=0)
    
    # Process and resize all the videos
    video_clips = []
    for video in video_paths:
        try:
            clip = mp.VideoFileClip(video)
            clip = resize_clip(clip, output_resolution)
            video_clips.append(clip)
            print(f"Video processed successfully: {video}")
        except Exception as e:
            print(f"Failed to process video: {video}, Error: {e}")

    if not video_clips:
        print("No videos processed successfully.")
        return None, None

    return video_clips, order_matrix

def concatenate_videos(video_paths, output_resolution, output_path, order_matrix):
    video_clips, order_matrix = process_videos_and_image(video_paths, output_resolution, order_matrix)
    
    if video_clips is None:
        return order_matrix

    # Concatenate the videos
    final_clips = []
    for i, video_clip in enumerate(video_clips):
        final_clips.append(video_clip)

    # Combine all clips into a final video
    final_video = mp.concatenate_videoclips(final_clips)

    # Write the final video to a file
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    return order_matrix

def get_video_files_from_csvs(csv_directory):
    video_files = []
    block_numbers = []
    video_ids = []
    # Get all CSV files in the directory and shuffle them to ensure random selection
    csv_files = [csv_file for csv_file in os.listdir(csv_directory) if csv_file.endswith('.csv')]
    random.shuffle(csv_files)
    
    # Iterate over shuffled CSV files
    for csv_file in csv_files:
        csv_path = os.path.join(csv_directory, csv_file)
        # Extract the block number from the file name (e.g., "A_block_3" extracts "3")
        block_number = int(csv_file.split('_')[2])
        # Extract the video id from the file name (e.g., "3.csv" extracts "3")
        video_id = os.path.splitext(csv_file)[0]
        # Read the CSV file and shuffle the rows to ensure pseudo-random order
        df = pd.read_csv(csv_path).sample(frac=1).reset_index(drop=True)
        # Get the list of video paths from the 'movie_path' column
        video_paths = df['movie_path'].tolist()
        video_files.extend(video_paths)
        block_numbers.extend([block_number] * len(video_paths))
        video_ids.extend([video_id] * len(video_paths))
    
    # Convert relative paths to absolute paths
    video_files = [os.path.abspath(os.path.join(base_dir, path)) for path in video_files]
    
    # Create a DataFrame with video files, block numbers, and video ids
    video_files_df = pd.DataFrame({'video_files': video_files, 'block_number': block_numbers, 'video_id': video_ids})
    
    return video_files_df

base_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f'{base_dir}/output_videos', exist_ok=True)

# Path to the directory containing all CSV files
csv_directory = r'C:\Users\Cocudata\experiment_VR\conditions\A'

# Get video files from all CSVs in the directory
video_files_df = get_video_files_from_csvs(csv_directory)
video_files = video_files_df['video_files'].tolist()
output_resolution = (1280, 720)  # Target resolution (width, height)
order_matrix = pd.DataFrame()

# Change range to get n output_videos
for n in range(1):
    output_file = f'{base_dir}/output_videos/output_video-{n}.mp4'
    order_matrix = concatenate_videos(video_files, output_resolution, output_file, order_matrix)

# Add video files, block numbers, and video ids to the order matrix
order_matrix = pd.DataFrame({
    'video_files': video_files_df['video_files'],
    'block_number': video_files_df['block_number'],
    'video_id': video_files_df['video_id']
})

order_matrix.to_excel(f'{base_dir}/order_matrix.xlsx')


#%%