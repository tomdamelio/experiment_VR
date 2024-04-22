#%%
import os
import ffmpeg
import pandas as pd

def trim_and_merge_video(video_path, audio_path, start_time, end_time, output_video_path):
    print(f"Processing video: {video_path} and audio: {audio_path}")
    try:
        if not os.path.exists(video_path) or not os.path.exists(audio_path):
            print(f"One or more files do not exist: {video_path}, {audio_path}")
            return

        video_stream = ffmpeg.input(video_path, ss=start_time, t=end_time - start_time)
        audio_stream = ffmpeg.input(audio_path, ss=start_time, t=end_time - start_time)
        ffmpeg.output(video_stream, audio_stream, output_video_path, vcodec='copy', acodec='aac').run(overwrite_output=True)
        print(f"Merged video saved to {output_video_path}")
    except ffmpeg.Error as e:
        print(f"Error merging {video_path} and {audio_path}: {e.stderr}")

def process_video(video_id, start_time, end_time, source_dir, target_dir):
    print(f"Processing ID: {video_id}")
    files = os.listdir(source_dir)
    video_files = [f for f in files if f.startswith(f"{video_id}_") and f.endswith('.mp4')]
    video_360_file = next((f for f in video_files if f.endswith('360.mp4')), None)
    audio_file = next((f for f in files if f.startswith(f"{video_id}_") and f.endswith('audio.mp4')), None)

    # Process 2D video
    video_2d_file = next((f for f in video_files if not f.endswith('360.mp4')), None)
    if video_2d_file:
        video_2d_path = os.path.join(source_dir, video_2d_file)
        target_video_2d_path = os.path.join(target_dir, video_2d_file.replace('.mp4', '_cropped.mp4'))
        print(f"Trimming 2D video {video_2d_path}")
        if os.path.exists(video_2d_path):
            ffmpeg.input(video_2d_path, ss=start_time, t=end_time - start_time).output(target_video_2d_path, vcodec='copy', acodec='aac').run(overwrite_output=True)
            print(f"Cropped 2D video saved to {target_video_2d_path}")
    
    # Merge 360 video with audio
    if video_360_file and audio_file:
        video_360_path = os.path.join(source_dir, video_360_file)
        audio_path = os.path.join(source_dir, audio_file)
        output_360_with_audio = os.path.join(target_dir, video_360_file.replace('.mp4', '_with_audio.mp4'))
        print(f"Merging 360 video {video_360_path} and audio {audio_path}")
        trim_and_merge_video(video_360_path, audio_path, start_time, end_time, output_360_with_audio)

# Load the data from an Excel file
df = pd.read_excel('df_with_validity_checks_2024_Tomi_selected_practice.xlsx')

# Filter rows where 'Selected' is 'yes'
#selected_df = df[df['Selected'] == 'yes']
selected_df = df[df['Practice_video'] == 'yes']


# Function to convert 'mm:ss' format to total seconds
def time_to_seconds(time_str):
    min, sec = map(int, time_str.split(':'))
    return min * 60 + sec

# Directory paths
source_dir = './vr_video_selected'
#source_dir = './practice_videos/vr_videos_selected_practice'
target_dir = './vr_video_selected_crop'
#target_dir = './practice_videos/vr_video_selected_practice_crop'

# Ensure target directory exists
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Process each selected video
for index, row in selected_df.iterrows():
    video_id = row['id']
    good_track = row['good_track']
    start_time, end_time = map(time_to_seconds, good_track.split('-'))
    process_video(str(video_id), start_time, end_time, source_dir, target_dir)


#%%