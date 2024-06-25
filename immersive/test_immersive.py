import logging
from psychopy import visual, core, event

# Initialize logging using Python's standard logging module
logging.basicConfig(level=logging.DEBUG)


    
# Create a window for the Rift
win = visual.Window(
    size=visual.Rift().size, fullscr=True, screen=0,
    monitor='testMonitor', units='norm', useFBO=True, allowStencil=True
)

logging.info("Window created successfully")

# Create a movie stimulus for the VR environment
video_path = "C:/Users/Cocudata/videos_360/8.mp4"  # Replace with your video file path
movie = visual.MovieStim3(win, video_path, size=(1.0, 1.0), flipVert=False, flipHoriz=False)

logging.info("MovieStim3 created successfully")

# Main loop to play the video
while movie.status != visual.FINISHED:
    # Draw the current frame of the movie
    movie.draw()

    # Update the window and display the frame in the Rift
    win.flip()

    # Handle events (e.g., check for 'escape' key to exit)
    keys = event.getKeys()
    if 'escape' in keys:
        break

logging.info("Video finished playing or 'escape' key pressed")

# Clean up and close the Rift session
win.close()
Rift().close()
core.quit()

