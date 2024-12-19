#%%
# # -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:13:30 2024

"""

import os
import cv2
import numpy as np
from scipy.io.wavfile import write
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def generate_whistle_sound(duration_sec, sample_rate=44100, freq=500):
    # Generate time array
    t = np.linspace(0, duration_sec, int(duration_sec * sample_rate), endpoint=False)

    # Generate whistle signal
    whistle_signal = np.sin(2 * np.pi * freq * t)

    # Scale signal to 16-bit range
    whistle_signal = np.int16(whistle_signal * 32767)

    return sample_rate, whistle_signal

# Parameters for the whistle sound
duration_sec = 1
sample_rate, whistle_signal = generate_whistle_sound(duration_sec)

# Save whistle sound to file
write("whistle_sound.wav", sample_rate, whistle_signal)

#%%

def create_black_screen_video(duration_sec, output_file, fps=30, width=640, height=360):
    # Calculate number of frames
    num_frames = int(duration_sec * fps)

    # Create VideoWriter object
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Create black frame
    black_frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Write black frames to video
    for _ in range(num_frames):
        out.write(black_frame)

    # Release VideoWriter
    out.release()

# Create black screen video of 1 second duration
#create_black_screen_video(1, "black_screen_1_sec.mp4")

#%%

def add_audio_to_video(video_file, audio_file, output_file):
    # Load the video clip
    video_clip = VideoFileClip(video_file)

    # Load the audio clip
    audio_clip = AudioFileClip(audio_file)

    # Set audio duration to match video duration
    audio_clip = audio_clip.set_duration(video_clip.duration)

    # Add audio to video
    video_with_audio = video_clip.set_audio(audio_clip)

    # Write final video with audio
    video_with_audio.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=video_clip.fps)



# Add audio to the black screen video

#add_audio_to_video("black_screen_1_sec.mp4", "whistle_sound.wav", "black_screen_with_audio.mp4")

#%%

def append_videos(video1_file, video2_file, output_file, fps=30, codec="libx264", audio_codec='aac'):
    # Load video clips
    video1_clip = VideoFileClip(video1_file)
    video2_clip = VideoFileClip(video2_file)

    # Set the frame rate for the output video
    video2_clip = video2_clip.set_fps(fps)

    # Concatenate video clips
    final_clip = concatenate_videoclips([video1_clip, video2_clip, video1_clip])

    # Write final video to file, ensuring to specify both video and audio codecs
    final_clip.write_videofile(output_file, codec=codec, audio_codec=audio_codec)


# Append video_1.mp4 to the beginning of video_2.mp4


#%%

def process_videos_in_folder(folder_path):
    # Iterate over files in the folder
    
    for filename in os.listdir(folder_path):
        # Check if the file is a video file
        if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
            # Process the video file (you can replace print with any processing logic)
            print("Processing video:", filename)
            
            video = cv2.VideoCapture(f'{folder_path}/{filename}')
            width_vid = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height_vid = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f'Width: {width_vid}')
            print(f'Height: {height_vid}')
            
            create_black_screen_video(1, "black_screen_1_sec.mp4", width=width_vid, height=height_vid)
            add_audio_to_video("black_screen_1_sec.mp4", "whistle_sound.wav", "black_screen_with_audio.mp4")
            
            append_videos("black_screen_with_audio.mp4", f'{folder_path}/{filename}', f'final_videos/{filename}')

#%%
folder_path = "videos"
process_videos_in_folder(folder_path)

#os.mkdir("final_videos")
#%%