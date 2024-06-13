import argparse
import pathlib
import ssl
import subprocess
from urllib.parse import urlparse
import requests
from pytube import YouTube
from pytube.extract import video_id

YT_DLP_OPTIONS_DEFAULT = ('--extract-audio --audio-format m4a --audio-quality 48k'
                          ' --embed-thumbnail --console-title --embed-metadata'
                          ' --newline --progress-delta 2 --break-on-existing')


def get_youtube_move_id(url: str):
    try:
        movie_id = video_id(url)
    except Exception as e:
        return None
    return movie_id


def download_audio(movie_id: str, folder: str, ytdlprewriteoptions: str = YT_DLP_OPTIONS_DEFAULT):
    data_dir = pathlib.Path(folder)
    data_dir.mkdir(parents=True, exist_ok=True)

    m4a_file = data_dir.joinpath(f'{movie_id}.m4a')
    if m4a_file.exists():
        print(f'💚 Audio file yet exists: {m4a_file}')
        return m4a_file.as_posix()

    url = f'https://www.youtube.com/watch?v={movie_id}'

    command = f'yt-dlp {ytdlprewriteoptions} --output {m4a_file.as_posix()} {url}'
    print('💙️ The audio download is starting...')
    print('[bash command yt-dlp] ', command)
    process = subprocess.Popen(
        command.split(' '),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)

    for line in process.stdout:
        print(line, end='')

    for line in process.stderr:
        print(line, end='')

    return m4a_file


def download_thumbnail(movie_id: str, folder: str):
    folder = pathlib.Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    thumbnail = folder.joinpath(f'{movie_id}.jpg')

    if thumbnail .exists():
        print(f'💚 Thumbnail file yet exists: {thumbnail}')
        return thumbnail.as_posix()

    # Special SSL setting to make valid HTTP request to Youtube server.
    ssl._create_default_https_context = ssl._create_stdlib_context

    yt = None
    try:
        yt = YouTube.from_id(movie_id)
        print('💙️ The thumbnail download is starting... \n', yt.thumbnail_url)
    except Exception as e:
        print(f"🟥 Error downloading thumbnail [YouTube.from_id(movie_id)]:\n {str(e)}")
        return

    try:
        response = requests.get(yt.thumbnail_url)
        if response.status_code == 200:
            with thumbnail.open('wb') as f:
                f.write(response.content)
        else:
            print(f"🟥 Failed to download image [response = requests.get(yt.thumbnail_url)].")
            print(f"Status code: {response.status_code}")
            return
    except Exception as e:
        print(f"🟥 Failed to download image [response = requests.get(yt.thumbnail_url)]:\n {str(e)}")
        return

    return thumbnail


def full_download(url, folder, ytdlprewriteoptions):
    context = dict()
    if not urlparse(url).netloc:
        print('⛔️ No URL in your request.')
        return context

    if not (movie_id := get_youtube_move_id(url)):
        print('⛔️ Its not a youtube URL. Check it again.')
        return context

    audio = download_audio(movie_id, folder, ytdlprewriteoptions)

    if not audio.exists():
        print(f'🟥 Unexpected error. After Check m4a_file.exists.')
        return context

    context['audio'] = audio

    thumbnail = download_thumbnail(movie_id, folder)
    if thumbnail.exists():
        print(f'🟥 Unexpected error. After Check thumbnail.exists().')
        return context

    context['thumbnail'] = thumbnail

    return context


def main():
    parser = argparse.ArgumentParser(description='Downloading Youtube audio and its thumbnail')
    parser.add_argument('url', type=str, help='Youtube URL with movie_id.')
    parser.add_argument('--folder', type=str,
                        help='Path to folder to save outputs. '
                             'Default is \".\"', default='.')
    parser.add_argument('--ytdlprewriteoptions', type=str,
                        help=f'Set no a default YT_DPL options in quotes. '
                             f'Default value is \"{YT_DLP_OPTIONS_DEFAULT}\". '
                             f'See full options https://github.com/yt-dlp/yt-dlp.',
                        default=f'{YT_DLP_OPTIONS_DEFAULT}')
    args = parser.parse_args()

    results = full_download(args.url, args.folder, args.ytdlprewriteoptions)
    if audio := results.get('audio'):
        print(audio)
    if thumbnail := results.get('thumbnail'):
        print(thumbnail)


if __name__ == "__main__":
    main()
