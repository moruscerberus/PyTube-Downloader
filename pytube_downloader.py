from pytubefix import YouTube
from colorama import init, Fore
import sys


def progress(count, total, suffix=''):
    bar_len = 60

    if total <= 0:
        return

    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)

    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write(
        '[%s] %s%% %s\r' %
        (bar, percents, suffix)
    )
    sys.stdout.flush()


def on_complete(stream, filepath):
    print('\n')
    print('Download complete!')
    print(f'File: {filepath}\n')


def on_progress(stream, chunk, bytes_remaining):
    try:
        total = stream.filesize
        downloaded = total - bytes_remaining
        progress(downloaded, total)
    except Exception:
        pass


# --------------------------------------------------
# START
# --------------------------------------------------

init(autoreset=True)

link = input('Youtube link: ').strip()

if not link:
    print(Fore.RED + 'No YouTube link was entered.')
    sys.exit(1)


# --------------------------------------------------
# CREATE YOUTUBE OBJECT
# --------------------------------------------------

try:
    video_object = YouTube(
        link,
        on_complete_callback=on_complete,
        on_progress_callback=on_progress
    )

except Exception as e:
    print(Fore.RED + f'\nCould not open YouTube video:')
    print(Fore.RED + str(e))
    sys.exit(1)


# --------------------------------------------------
# VIDEO INFORMATION
# --------------------------------------------------

try:
    print(Fore.RED + f'title:  \033[39m {video_object.title}')
    print(
        Fore.RED +
        f'length: \033[39m {round(video_object.length / 60, 2)} minutes'
    )
    print(
        Fore.RED +
        f'views:  \033[39m {video_object.views / 1000000:.2f} million'
    )
    print(Fore.RED + f'author: \033[39m {video_object.author}')

except Exception as e:
    print(Fore.RED + f'\nCould not retrieve video information:')
    print(Fore.RED + str(e))
    sys.exit(1)


# --------------------------------------------------
# DOWNLOAD MENU
# --------------------------------------------------

print()

print(
    Fore.RED + 'download: ' +
    Fore.GREEN + '(ba) best [WEBM] (No Audio) \033[39m| ' +
    Fore.GREEN + '(b)  best [MP4]  (No Audio) \033[39m| ' +
    Fore.YELLOW + '(g)  good [MP4]  (Audio) \033[39m| ' +
    Fore.YELLOW + '(d)  low quality [MP4] (Audio) \033[39m| ' +
    Fore.BLUE + '(a)  audio only \033[39m| ' +
    '(e) exit'
)

download_choice = input('choice: ').strip().lower()

location = r''


# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

match download_choice:

    # ----------------------------------------------
    # BEST WEBM VIDEO
    # ----------------------------------------------

    case 'ba':

        print('\nFinding best WEBM video stream...')

        stream = (
            video_object.streams
            .filter(
                progressive=False,
                file_extension='webm',
                only_video=True
            )
            .order_by('resolution')
            .last()
        )

        if stream is None:
            print(Fore.RED + 'No WEBM video stream found.')
            sys.exit(1)

        print(f'Downloading: {stream}')

        try:
            stream.download(output_path=location)
        except Exception as e:
            print(Fore.RED + f'Download failed: {e}')


    # ----------------------------------------------
    # BEST MP4 VIDEO
    # ----------------------------------------------

    case 'b':

        print('\nFinding best MP4 video stream...')

        stream = (
            video_object.streams
            .filter(
                progressive=False,
                file_extension='mp4',
                only_video=True
            )
            .order_by('resolution')
            .last()
        )

        if stream is None:
            print(Fore.RED + 'No MP4 video stream found.')
            sys.exit(1)

        print(f'Downloading: {stream}')

        try:
            stream.download(output_path=location)
        except Exception as e:
            print(Fore.RED + f'Download failed: {e}')


    # ----------------------------------------------
    # GOOD MP4 WITH AUDIO
    # ----------------------------------------------

    case 'g':

        print('\nFinding MP4 stream with audio...')

        # First try a progressive stream.
        # Progressive = video + audio in one file.
        stream = (
            video_object.streams
            .filter(
                progressive=True,
                file_extension='mp4'
            )
            .order_by('resolution')
            .last()
        )

        if stream is not None:

            print(f'Downloading: {stream}')

            try:
                stream.download(output_path=location)
            except Exception as e:
                print(Fore.RED + f'Download failed: {e}')

        else:

            print(
                Fore.YELLOW +
                'No progressive MP4 stream is available for this video.'
            )

            print(
                Fore.YELLOW +
                'The video and audio are provided as separate streams.'
            )

            print(
                Fore.YELLOW +
                'Downloading the best video stream instead...'
            )

            stream = (
                video_object.streams
                .filter(
                    file_extension='mp4',
                    only_video=True
                )
                .order_by('resolution')
                .last()
            )

            if stream is None:
                print(Fore.RED + 'No suitable MP4 video stream found.')
                sys.exit(1)

            print(f'Downloading: {stream}')

            try:
                stream.download(output_path=location)

                print()
                print(
                    Fore.YELLOW +
                    'NOTE: This file contains video only.'
                )
                print(
                    Fore.YELLOW +
                    'For automatic video + audio merging, use yt-dlp + FFmpeg.'
                )

            except Exception as e:
                print(Fore.RED + f'Download failed: {e}')


    # ----------------------------------------------
    # LOWEST QUALITY
    # ----------------------------------------------

    case 'd':

        print('\nFinding lowest quality stream...')

        stream = (
            video_object.streams
            .filter(progressive=True)
            .order_by('resolution')
            .first()
        )

        if stream is None:

            stream = (
                video_object.streams
                .filter(
                    file_extension='mp4',
                    only_video=True
                )
                .order_by('resolution')
                .first()
            )

        if stream is None:
            print(Fore.RED + 'No suitable stream found.')
            sys.exit(1)

        print(f'Downloading: {stream}')

        try:
            stream.download(output_path=location)
        except Exception as e:
            print(Fore.RED + f'Download failed: {e}')


    # ----------------------------------------------
    # AUDIO ONLY
    # ----------------------------------------------

    case 'a':

        print('\nFinding audio stream...')

        stream = video_object.streams.get_audio_only()

        if stream is None:
            print(Fore.RED + 'No audio stream found.')
            sys.exit(1)

        print(f'Downloading: {stream}')

        try:
            stream.download(output_path=location)
        except Exception as e:
            print(Fore.RED + f'Download failed: {e}')


    # ----------------------------------------------
    # EXIT
    # ----------------------------------------------

    case 'e':

        print('Exiting.')
        sys.exit(0)


    # ----------------------------------------------
    # INVALID CHOICE
    # ----------------------------------------------

    case _:

        print(Fore.RED + 'Invalid choice.')
        print('Use: ba, b, g, d, a, or e')
        sys.exit(1)
