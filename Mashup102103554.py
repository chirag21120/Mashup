import sys
import os
import subprocess
from pytube import Search
from pytube import YouTube
from pydub import AudioSegment

def download_videos(singer_name, num_videos):
    query = f'{singer_name} songs'
    try:
        search_results = Search(query).results
        urls = [f'https://www.youtube.com/watch?v={result.video_id}' for result in search_results[:num_videos]]
        for url in urls:
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            video.download()
            print(f'Downloaded: {url}')
    except Exception as e:
        print(f'Error downloading videos: {e}')
        sys.exit(1)

def convert_to_audio():
    for file in os.listdir():
        if file.endswith(".mp4"):
            try:
                subprocess.run(['ffmpeg', '-i', file, f'{file[:-4]}.mp3'])
                os.remove(file)
            except Exception as e:
                print(f'Error converting {file} to audio: {e}')

def cut_audio(duration):
    print("Files in directory before conversion:", os.listdir())
    for file in os.listdir():
        if file.endswith(".mp3"):
            try:
                audio = AudioSegment.from_mp3(file)
                cut_audio = audio[:duration * 1000]
                cut_audio.export(f'cut_{file}', format="mp3")
                os.remove(file)
            except Exception as e:
                print(f'Error cutting audio from {file}: {e}')
    print("Files in directory after conversion:", os.listdir())

def merge_audios(output_filename):
    print("Files in directory before merging:", os.listdir())
    audio_files = [file for file in os.listdir() if file.startswith("cut_")]
    try:
        merged = None
        for file in audio_files:
            audio = AudioSegment.from_mp3(file)
            if merged is None:
                merged = audio
            else:
                merged = merged + audio
            os.remove(file)
        merged.export(output_filename, format="mp3")
        print(f'Merged audios saved as {output_filename}')
    except Exception as e:
        print(f'Error merging audios: {e}')

def main(singer_name, num_videos, audio_duration, output_filename):
    if num_videos <= 10:
        print("Number of videos should be greater than 10")
        return False

    if audio_duration <= 20:
        print("Audio duration should be greater than 20 seconds")
        return False

    download_videos(singer_name, num_videos)
    convert_to_audio()
    cut_audio(audio_duration)
    merge_audios(output_filename)
    return True

if __name__ == "__main__":
    main()
