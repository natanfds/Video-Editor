from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip


def apply_overlay(
    video: VideoFileClip,
    image: ImageClip,
) -> VideoFileClip:
    image.set_duration(video.duration)
    image.set_position((0, 0))
    res = CompositeVideoClip([video, image])
    return res
