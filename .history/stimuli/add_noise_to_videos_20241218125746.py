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

#%%

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

#%%

def create_flicker_screen_video(duration_sec, output_file, fps=30, width=640, height=360):
    num_frames = int(duration_sec * fps)
    # Crear VideoWriter
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    # Frames negros y blancos
    black_frame = np.zeros((height, width, 3), dtype=np.uint8)
    white_frame = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Calcular cuántos frames por medio ciclo
    cycles_per_second = 2
    frames_per_cycle = fps // cycles_per_second  # en este caso 30/5 = 6
    
    # Cada ciclo: mitad negro, mitad blanco
    half_cycle_frames = frames_per_cycle // 2  # 6/2 = 3
    
    # Generar los frames
    for i in range(num_frames):
        cycle_index = i % frames_per_cycle
        if cycle_index < half_cycle_frames:
            # Negro
            out.write(black_frame)
        else:
            # Blanco
            out.write(white_frame)
    
    out.release()



# Create black screen video of 1 second duration
#create_flicker_screen_video(1, "black_flicker_1_sec.mp4")

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
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
            print("Processing video:", filename)
            
            video = cv2.VideoCapture(f'{folder_path}/{filename}')
            width_vid = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height_vid = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Crear flicker 1 seg con audio
            create_flicker_screen_video(1, "flicker_1_sec.mp4", width=width_vid, height=height_vid)
            add_audio_to_video("flicker_1_sec.mp4", "whistle_sound.wav", "flicker_1_sec_with_audio.mp4")

            # Crear flicker 1 seg final con audio
            create_flicker_screen_video(1, "flicker_1_sec_final.mp4", width=width_vid, height=height_vid)
            add_audio_to_video("flicker_1_sec_final.mp4", "whistle_sound.wav", "flicker_1_sec_final_with_audio.mp4")

            # Crear black screen 30 seg
            create_black_screen_video(30, "black_screen_30_sec.mp4", width=width_vid, height=height_vid)
            
            # Concatenar: flicker_1_sec_with_audio + video original + flicker_1_sec_final_with_audio + black_screen_30_sec
            flicker_1_clip = VideoFileClip("flicker_1_sec_with_audio.mp4")
            original_clip = VideoFileClip(f'{folder_path}/{filename}')
            flicker_1_final_clip = VideoFileClip("flicker_1_sec_final_with_audio.mp4")
            black_30_clip = VideoFileClip("black_screen_30_sec.mp4")

            final_clip = concatenate_videoclips([flicker_1_clip, original_clip, flicker_1_final_clip, black_30_clip])
            final_clip.write_videofile(f'final_videos_2D/{filename}', codec='libx264', audio_codec='aac', fps=30)

#%%
folder_path = "videos_2D"
process_videos_in_folder(folder_path)

#os.mkdir("final_videos")
#%%

