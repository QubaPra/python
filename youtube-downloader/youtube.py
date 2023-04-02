from pytube import YouTube
import threading
import os
import time
from tkinter import Tk, filedialog
import pyperclip

down_audio = False

# get the URL from the clipboard
url = pyperclip.paste()

# check if the URL is a valid YouTube URL
if "youtube.com" not in url and "youtu.be" not in url:
    print("Invalid YouTube URL.")
    exit()

# create a YouTube object with the URL
yt = YouTube(url)

# get all available streams and sort by resolution in descending order
video = yt.streams.order_by('resolution').desc()

# create an empty list to keep track of unique streams
video_list = []

# loop through streams and print unique streams
print("Available Video:")
for i, stream in enumerate(video):
    if not((stream.mime_type == "video/webm" and len(stream.resolution) < 5) or stream.mime_type == "video/3gpp"):    
        stream_info = (stream.resolution, stream.mime_type, stream.abr, stream.fps)
        if stream_info not in video_list:
            video_list.append(stream_info)
            ext = (stream.mime_type).split("/")[-1]
            print(f"{len(video_list)}. {stream.resolution} {stream.fps}fps {ext} ({round(stream.filesize/(1024*1024))} MB) {'audio' if stream.abr else ''}")

# create an empty list to keep track of unique streams
audio = yt.streams.filter(only_audio=True).order_by('abr').desc()
audio_list = []

print("Available Audio:")
for i, stream in enumerate(audio):
    audio_list.append((stream.mime_type, stream.abr))
    ext = (stream.mime_type).split("/")[-1]
    print(f"{len(audio_list)+len(video_list)}. {stream.abr} {ext} ({round(stream.filesize/(1024*1024))} MB) audio")

# ask user to choose a stream to download
stream_num = input("Enter the number of the stream you want to download: ")

if stream_num[-1] == "a":
    stream_num = int(stream_num[:-1])
    down_audio = True
else:
    stream_num = int(stream_num)

if stream_num > len(video_list):
    selected_stream = audio.filter(mime_type=audio_list[stream_num-1-len(video_list)][0], abr=audio_list[stream_num-1-len(video_list)][1]).first()
else:
    selected_stream = video.filter(resolution=video_list[stream_num-1][0], mime_type=video_list[stream_num-1][1], abr=video_list[stream_num-1][2], fps=video_list[stream_num-1][3]).first()

# choose download directory with file dialog
root = Tk()
root.withdraw()
selected_directory = filedialog.askdirectory()
if selected_directory:
    os.chdir(selected_directory)

if down_audio:
    selected_astream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()    
    selected_astream.download(filename=selected_astream.default_filename.split('.')[0] + ' audio'+ selected_astream.default_filename[selected_astream.default_filename.rfind("."):])    

t1 = threading.Thread(target=selected_stream.download)
t1.start()

while True:
    if os.path.exists(selected_stream.default_filename):
        file_size = os.path.getsize(selected_stream.default_filename)
        print(f"{round(file_size / (1024 * 1024))} / {round(selected_stream.filesize / (1024 * 1024))} MB.", end='\r')
        if file_size == selected_stream.filesize:
            break
    time.sleep(1)  
t1.join()
print("Download complete!")