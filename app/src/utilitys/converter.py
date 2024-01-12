from pydub import AudioSegment
import io
from fastapi import UploadFile


def audio_webm_to_mp3(audiofile: UploadFile) -> UploadFile:
    webm_audio = AudioSegment.from_file(audiofile.file, format="webm")

    # Export AudioSegment as WAV file
    wav_buffer = io.BytesIO()
    webm_audio.export(wav_buffer, format="mp3")
    wav_buffer.seek(0)

    new_audiofile = UploadFile(
        filename=audiofile.filename,
        headers={"content-type": "audio/mp3"},
        file=wav_buffer,
    )

    return new_audiofile
