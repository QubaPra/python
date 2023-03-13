import pytube
from tkinter import filedialog, Tk

link = input("Enter the YouTube link: ")

yt = pytube.YouTube(link)

# Prompt the user to select whether to download audio or video
while True:
    download_type = input("Do you want to download audio (a) or video (v)? ")
    if download_type == "a":
        stream = yt.streams.filter(type="audio").order_by("abr").last()
        break
    elif download_type == "v":
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
        break

    else:
        print("Invalid choice. Please enter 'a' or 'v'.")

# Prompt the user to select a download location using a file dialog
root = Tk()
root.withdraw()
download_location = filedialog.askdirectory(title="Choose download location")

# Download the selected audio or video stream
stream.download(download_location)

print("Download complete.")
