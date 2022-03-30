from pytube import YouTube
from colorama import init, Fore
import time
import sys



def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

   
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben

def on_complete(stream, filepath):
    print('\n')
    print('download complete\n')

def on_progress(stream, chunk, bytes_remaining):
    progress(1, 1, bytes_remaining)


init()
link = input('Youtube link: ')
video_object = YouTube(link, 
on_complete_callback = on_complete,
on_progress_callback = on_progress)


# video information
print(Fore.RED + f'title:  \033[39m {video_object.title}')
print(Fore.RED + f'length: \033[39m {round(video_object.length / 60, 2)} minutes')
print(Fore.RED + f'views:  \033[39m {video_object.views / 1000000} million')
print(Fore.RED + f'author: \033[39m {video_object.author}')


# video streams
# for stream in video_object.streams:
#     print(stream)

#download
print(Fore.RED + 'download:' + 
Fore.GREEN + '(bn)est [WEBM] (No Audio)\033[39m| ' + 
Fore.GREEN + '(b)est [MP4] (No Audio)\033[39m|'+
Fore.YELLOW + '(g)ood enough [MP4] (Audio)\033[39m|' + 
Fore.YELLOW + '(d)disgusting [MP4] (Audio)\033[39m|' + 
Fore.BLUE + '(a)udio Only \033[39m| (e)xit')
download_choise = input('choice: ')

location = r''

match download_choise:
    case 'ba':
        video_object.streams.filter(progressive=False, file_extension='webm').order_by('resolution').last().download() # , file_extension='mp4'
    case 'b':
        video_object.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').last().download() # , file_extension='mp4'
    case 'g':
        video_object.streams.get_highest_resolution().download()
    case 'd':
        video_object.streams.get_lowest_resolution().download()
    case 'a':
        video_object.streams.get_audio_only().download()
  

