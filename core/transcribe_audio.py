import whisper_timestamped as whisper
from typing import TypedDict, List
import speech_recognition as sr
from threading import Thread


class WordInfo(TypedDict):
    start: float
    end: float
    text: str


def transcribe_audio_into_words(
    audio_path: str,
    speech_recog_model: str = "tiny",
    process_device: str = "cpu",
    language: str = "pt",
) -> List[WordInfo]:
    audio = whisper.load_audio(audio_path)
    model = whisper.load_model(speech_recog_model, device=process_device)
    result = whisper.transcribe(model, audio, language=language)
    segments = result["segments"]

    words = []

    for segment in segments:
        words = [*words, *segment["words"]]

    return words


def transcribe_audio_with_google(audio_path) -> dict:
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(
            audio_data,
            language="pt-BR",
            show_all=True
        )

    return text


class AudioTranscriptions(TypedDict):
    from_google: List[str]
    from_model: List[WordInfo]


def transcribe_audio(audio_path: str) -> AudioTranscriptions:
    threads = []
    transcription_google = None
    transcription_in_words = None

    def transcribe_google():
        nonlocal transcription_google
        transcription_google = transcribe_audio_with_google(audio_path)
        transcription_google = transcription_google[
            "alternative"][0]["transcript"]
        transcription_google = transcription_google.split(' ')

    def transcribe_model():
        nonlocal transcription_in_words
        transcription_in_words = transcribe_audio_into_words(audio_path)

    threads.append(Thread(target=transcribe_google))
    threads.append(Thread(target=transcribe_model))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    res = {
        "from_google": transcription_google,
        "from_model": transcription_in_words
    }

    return res
