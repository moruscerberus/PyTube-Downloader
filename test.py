from pytube import YouTube
yt = YouTube('https://www.youtube.com/watch?v=KiB0vRi2wlc')
for stream in yt.streams:
    print(stream)
yt.streams.filter(progressive=False, file_extension='webm').order_by('resolution').last().download() # , file_extension='mp4'