import moviepy.editor as mp
import random
import os
import pandas as pd

#%%

def resize_clip(clip, target_resolution):
    return clip.resize(target_resolution)

def process_videos_and_image(video_paths, output_resolution, order_matrix):
    # Shuffle the videos in a pseudo-random order (all videos selected exactly once)
    random.shuffle(video_paths)
    print(f'Orden: {video_paths}')
    order_matrix = pd.concat([order_matrix, pd.Series(video_paths)], axis=1)
    
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
        return

    # Concatenate the videos
    final_clips = []
    for i, video_clip in enumerate(video_clips):
        final_clips.append(video_clip)

    # Combine all clips into a final video
    final_video = mp.concatenate_videoclips(final_clips)

    # Write the final video to a file
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    return order_matrix

def get_video_files_from_csv(csv_path):
    # Read the CSV file and get the list of video paths from the 'movie_path' column
    df = pd.read_csv(csv_path)
    video_files = df['movie_path'].tolist()
    
    # Convert relative paths to absolute paths
    video_files = [os.path.abspath(os.path.join(base_dir, '..', path)) for path in video_files]
    
    return video_files

base_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f'{base_dir}/output_videos', exist_ok=True)

# Path to the CSV file containing video paths (corrected to the actual path)
csv_path = os.path.join(base_dir, '..', 'conditions', 'A', 'A_block_3_valence_right.csv')

# Get video files from CSV
video_files = get_video_files_from_csv(csv_path)

output_resolution = (1280, 720)  # Target resolution (width, height)
order_matrix = pd.DataFrame()

# Change range to get n output_videos
for n in range(1):
    output_file = f'{base_dir}/output_videos/output_video-{n}.mp4'
    order_matrix = concatenate_videos(video_files, output_resolution, output_file, order_matrix)

order_matrix.to_excel(f'{base_dir}/order_matrix.xlsx')


#%%