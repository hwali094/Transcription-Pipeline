# Transcription Pipeline

A simple script that takes an audio file (WAV or MP3), converts the speech to text, and also returns the text with a start and end time for each segment.

## How to run

```
pip install -r requirements.txt
python main.py
```

By default it transcribes `./test_audio/sample.wav`. Change `FILE_PATH` in `main.py` to try the other files (`sample.mp3`, `long.wav`). The first run downloads the model, so it takes a bit longer.

## What it does

1. `load_file` checks the file extension (wav or mp3), checks the file exists and reads it.
2. `transcribe_audio` returns the full text.
3. `transcribe_audio_with_timestamps` returns a list of segments, each with start, end and text.

## Choices

- I used `faster-whisper` because it is open source, runs locally, needs no API key and gives timestamps per segment.
- I used the `tiny` model on CPU because it is fast. A bigger model is more accurate but slower.
- I pass the file path to the library instead of bytes, because the library decodes WAV and MP3 by itself.

## Limits

- It only checks the file extension, not the real content. With more time I would check the file header too.
- The model is loaded on every call, it should be loaded once and reused.
- Long files are not split yet (see the design notes below).
- No tests, no API yet.

## Design notes

- **Different formats:** check the extension and the content, then convert only if the library can't read the format. If a file can't be decoded, fail with a clear error and don't retry.
- **Long audio files:** split the audio into chunks that overlap by a few seconds so no word is cut in half, transcribe each chunk, add the chunk's start time to its timestamps and join the results, removing the duplicated text.
- **Concurrent uploads:** put each upload on a queue (for example Redis with workers), return a job id right away and limit how many jobs run at once. The user gets the result by webhook or by checking the status.
- **Storage:** audio files go to S3 so the server doesn't run out of disk. The database has a table for the audio file and job status, and a separate table for transcripts (text, segments with timestamps, model used) linked by a foreign key.
- **Retries:** if the audio file itself is bad, mark it as corrupted and ask the user to upload again. For model or connection errors, retry up to 3 times with a small delay, then mark the job as failed with an error message.
- **API:** `POST /transcribe` (returns 202 and a job id), `GET /status/{id}`, `GET /transcript/{id}`. All need an API key, and uploads have a file size limit and a rate limit.
