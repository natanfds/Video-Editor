from ursina import Ursina, Entity, color, Button, camera, Slider, mouse
from ursina import *


app = Ursina()
current_time = 0
slider_in_use = False
video = "assets/sample.mp4"
video_player: Entity = Entity(
    model='quad',
    parent=camera.ui,
    scale=(1.5, 1),
    texture=video
)
video_sound = loader.loadSfx(video) # type: ignore
video_player.texture.synchronizeTo(video_sound)


btn_play = Button(
    text='>',
    color=color.azure,
    scale=(0.1, 0.05),
    position=(0.7, -0.4),
    z=-1
)


def on_btn_play_click():
    global current_time
    if video_sound.status() == 1:
        if current_time != 0:
            video_sound.setTime(current_time)
        if current_time == video_sound.length():
            current_time = 0
            video_sound.setTime(current_time)
        video_sound.play()


btn_play.on_click = on_btn_play_click

btn_stop = Button(
    text='[]',
    color=color.azure,
    scale=(0.1, 0.05),
    position=(0.6, -0.4),
    z=-1
)


def on_btn_stop_click():
    global current_time
    if video_sound.status() == 2:
        current_time = 0
        video_sound.stop()


btn_stop.on_click = on_btn_stop_click


btn_pause = Button(
    text='||',
    color=color.azure,
    scale=(0.1, 0.05),
    position=(0.8, -0.4),
    z=-1
)


def on_btn_pause_click():
    global current_time
    if video_sound.status() == 2:
        current_time = video_sound.getTime()
        video_sound.stop()


btn_pause.on_click = on_btn_pause_click

progress_bar = Slider(
    min=0,
    max=video_sound.length(),
    default=0,
    step=0.01,
    dynamic=True,
    position=(0, -0.4),
    scale=(0.6, 0.6),
    z=-1
)


def on_slider_change():
    global slider_in_use
    global current_time
    if slider_in_use:
        video_sound.stop()
        current_time = progress_bar.value
        video_sound.setTime(current_time)
        video_sound.play()


progress_bar.on_value_changed = on_slider_change


def update():
    global slider_in_use
    if mouse.left:
        slider_in_use = True
    else:
        slider_in_use = False

    if not slider_in_use:
        progress_bar.value = video_sound.getTime()


app.run()
