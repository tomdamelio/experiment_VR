#%%
from psychopy import visual, core, event

# Crear una ventana
win = visual.Window(size=(800, 600), fullscr=True, allowGUI=False)

# Cargar el video
video_path = '../stimuli/vr_videos/14.0_1080p_24fps_War Zone.mp4'
movie = visual.MovieStim3(win, video_path, size=(1920, 1080), flipVert=False)

# Reproducir el video
while movie.status != visual.FINISHED:
    movie.draw()
    win.flip()
    if event.getKeys(keyList=["escape", "q"]):
        break

# Cerrar la ventana y salir
win.close()
core.quit()

#%%q