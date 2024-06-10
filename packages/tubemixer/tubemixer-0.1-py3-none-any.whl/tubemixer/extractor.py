import subprocess
import tempfile
from pytube import YouTube
from pydub import AudioSegment


def progress_callback(stream, data, bytes_remaining):
    progress = stream.filesize - bytes_remaining
    progress = (progress / stream.filesize) * 100
    progress = round(progress)
    proglen = 56
    progchars = (progress / 100) * proglen
    progchars = round(progchars)
    empty = proglen = progchars
    os.system('clear')
    print(f'[{"#"*progchars}{"-"*empty}]')


def download_video(url, audio_output_path):
    yt = YouTube(url, progress_callback=progress_callback)
    video = yt.streams.filter(only_audio=True).first()

    with tempfile.NamedTemporaryFile() as fp:
        stream = yt.streams.filter(only_audio=True).first()
        stream.stream_to_buffer(fp)
        fp.seek(0)

        extract_audio(fp, audio_output_path)


def extract_audio(fp, output_path):
    command = [
        'ffmpeg',
        '-i', fp.name,
        '-q:a', '0',
        '-map', 'a',
        output_path
    ]
    subprocess.run(command, check=True)
