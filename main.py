from moviepy.editor import VideoFileClip
from core.transcribe_audio import transcribe_audio


def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


def main():
    video_path = "assets/sample.mp4"
    audio_path = "extracted_audio.wav"
    extract_audio(video_path, audio_path)
    res = transcribe_audio(audio_path)
    print(res)


if __name__ == "__main__":
    main()
