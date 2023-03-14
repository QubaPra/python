import pytube
from tkinter import filedialog, Tk
import os
import time
import math
import sys

def progress_callback(stream, chunk, bytes_remaining):
    # Get the total file size in bytes
    total_size = stream.filesize
    
    # Calculate the bytes downloaded so far
    bytes_downloaded = total_size - bytes_remaining
    
    # Calculate the percentage of download
    percent = (bytes_downloaded / total_size) * 100.0
    
    # Calculate the download speed in bytes per second
    download_speed = (bytes_downloaded / (time.time() - start_time))
    
    # Calculate the estimated time remaining in seconds
    time_remaining = bytes_remaining / download_speed
    
    # Convert to minutes and seconds
    minutes, seconds = divmod(time_remaining, 60)
    
    # Calculate the size of the file in megabytes
    file_size_mb = total_size / (1024 * 1024)
    
    # Calculate the number of megabytes downloaded
    downloaded_mb = bytes_downloaded / (1024 * 1024)
    
    # Print the progress bar
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%  %.2fMB/%.2fMB  %.2fMB/s  ETA: %d:%02d" % ('='*int(20*percent/100), percent, downloaded_mb, file_size_mb, download_speed/(1024*1024), minutes, seconds))
    sys.stdout.flush()

link = input("Enter the YouTube link: ")

yt = pytube.YouTube(link)

# Prompt the user to select whether to download audio or video
download_type = input("Do you want to download audio (a) or video (v)? ")
audio = yt.streams.filter(type="audio").order_by("abr").last()

if download_type == "v":
    # Filter and print out only the video streams, sorted by resolution
    video_streams = yt.streams.filter(type="video").order_by("resolution").desc()
    stream_info = {}
    for stream in video_streams:
        if stream.resolution == "2160p":
            ext = stream.mime_type.split('/')[-1]
        elif stream.resolution == "1440p":
            ext = stream.mime_type.split('/')[-1]
        else:
            ext = "mp4"
        stream_info[f"{stream.resolution} {stream.fps}fps {ext}"] = stream

    for i, info in enumerate(stream_info.keys()):
        print(f"{i}: {info}")

    # Prompt the user to select a video stream to download
    stream_num = int(input("Enter the stream number to download: "))
    stream = list(stream_info.values())[stream_num]

# Prompt the user to select a download location using a file dialog
root = Tk()
root.withdraw()
download_location = filedialog.askdirectory(title="Choose download location")

if download_type == "a":
    start_time = time.time()
    # Download the selected audio stream
    audio.download(download_location, filename=audio.default_filename.split('.')[0] + ' audio'+ audio.default_filename[audio.default_filename.rfind("."):], 
                   on_progress_callback=progress_callback)
else:
    start_time = time.time()
    # Download the selected video stream
    stream.download(download_location, 
                    filename=stream.default_filename.split('.')[0] + ' video'+ stream.default_filename[stream.default_filename.rfind("."):],
                    on_progress_callback=progress_callback)

# Print the final progress bar with 100% completion
sys.stdout.write('\r')
sys.stdout.write("[%-20s] %d%%  %.2fMB/%.2fMB  %.2fMB/s  ETA: 00:00" % ('='*20, 100, file_size_mb, file_size_mb, 0))
sys.stdout.flush()

print("\nDownload complete.")

