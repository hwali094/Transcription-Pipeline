from faster_whisper import WhisperModel

FILE_PATH = "./test_audio/long.wav"

def load_file(path):
    """loads an audio file and returns its binary data. Raises an error if the file is not found or if the file format is not supported."""
    file_extension = path.split(".")[-1]
    file_extension = file_extension.lower()

    if not file_extension in ["wav", "mp3"]:
        raise ValueError("Unsupported audio format")

    try:
        with open(path, "rb") as f:
            return f.read()

    except FileNotFoundError:
        raise FileNotFoundError("File not found")

def transcribe_audio(file_path):
    """transcribes the audio data using the faster-whisper library and returns the transcription as a string."""
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, info = model.transcribe(file_path, beam_size=5)

    transcription = ""
    for segment in segments:
        transcription += segment.text + " "

    return transcription.strip()

def transcribe_audio_with_timestamps(path):
    """transcribes the audio data using the faster-whisper library and returns the transcription with timestamps."""
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, info = model.transcribe(path, beam_size=5)

    transcription_with_timestamps = []
    for segment in segments:
        transcription_with_timestamps.append({
            "segment_start": segment.start,
            "segment_end": segment.end,
            "segment_text": segment.text
        })

    return transcription_with_timestamps


audio_data = load_file(FILE_PATH)
if audio_data:
    print("Audio file loaded successfully.")
    transcription = transcribe_audio(FILE_PATH)
    print("Transcription:", transcription)

    transcription_with_timestamps = transcribe_audio_with_timestamps(FILE_PATH)
    print("Transcription with timestamps:")
    for segment in transcription_with_timestamps:
        print(f"Start: {segment['segment_start']}, End: {segment['segment_end']}, Text: {segment['segment_text']}")
else:
    raise ValueError("Audio file is empty")
