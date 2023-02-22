import tkinter as tk
from tkinter import *
from pytube import YouTube
from tkinter import messagebox, filedialog
import os
import ffmpeg
#import moviepy.editor as mpe
from moviepy.editor import *


def Widgets():
    head_label = Label(root, text="YouTube Video And Audio Downloader",
                       padx=15,
                       pady=30,
                       font="SegoeUI 14",
                       bg="gray",
                       fg="black")
    head_label.grid(row=1,
                    column=1,
                    pady=0,
                    padx=0,
                    columnspan=3)

    link_label = Label(root,
                       text="YouTube link :",
                       bg="gray",
                       pady=5,
                       padx=5)
    link_label.grid(row=2,
                    column=0,
                    pady=5,
                    padx=5)

    root.linkText = Entry(root,
                          width=35,
                          textvariable=video_Link,
                          font="Arial 14")
    root.linkText.grid(row=2,
                       column=1,
                       pady=5,
                       padx=5,
                       columnspan=2)

    destination_label = Label(root,
                              text="Destination folder :",
                              bg="gray",
                              pady=5,
                              padx=9)
    destination_label.grid(row=3,
                           column=0,
                           pady=5,
                           padx=5)

    root.destinationText = Entry(root,
                                 width=27,
                                 textvariable=download_Path,
                                 font="Arial 14")
    root.destinationText.grid(row=3,
                              column=1,
                              pady=5,
                              padx=5)

    browse_B = Button(root,
                      text="Browse",
                      command=Browse,
                      width=10,
                      bg="white",
                      relief=GROOVE)
    browse_B.grid(row=3,
                  column=2,
                  pady=1,
                  padx=1)

    #######################################################################################

    destination_label = Label(root,
                              text="Choose resolution :",
                              bg="gray",
                              pady=5,
                              padx=9)
    destination_label.grid(row=4,
                           column=0,
                           pady=5,
                           padx=5)

    video_res.set("resolution")
    drop = OptionMenu(root, video_res, "144p", "240p", "360p", "480p", "720p", "1080p", command=Set_res)
    drop.grid(row=4,
              column=1,
              pady=5,
              padx=5)

    #######################################################################################

    Download_B = Button(root,
                        text="Download Video",
                        command=Download,
                        width=20,
                        bg="white",
                        pady=10,
                        padx=15,
                        relief=GROOVE,
                        font="Georgia, 13")
    Download_B.grid(row=5,
                    column=1,
                    pady=20,
                    padx=20)

    Download_audio_B = Button(root,
                        text="Download Audio",
                        command=Download_audio,
                        width=20,
                        bg="white",
                        pady=10,
                        padx=15,
                        relief=GROOVE,
                        font="Georgia, 13")
    Download_audio_B.grid(row=6,
                    column=1,
                    pady=20,
                    padx=20)


def Browse():

    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save Video")
    download_Path.set(download_Directory)


def Set_res(value):
    """
    resolutions=[]
    Youtube_link = video_Link.get()
    getVideo = YouTube(Youtube_link)
    for stream in getVideo.streams:
        resolutions.append(stream.resolution)
    print(resolutions)
    if value in resolutions:
        print("correct")
    else:
        print("wrong")
    """


def Download():

    Youtube_link = video_Link.get()

    download_Folder = download_Path.get()

    getVideo = YouTube(Youtube_link)
    resolution = video_res.get()
    video = getVideo.streams.filter(res=resolution).first()
    audio = getVideo.streams.filter(only_audio=True).first()

    video_name = video.default_filename
    audio_name_init = audio.default_filename
    base, ext = os.path.splitext(audio_name_init)
    audio_name = base + "_audio" + '.mp3'
    print(audio_name)

    if video is None:
        messagebox.showinfo("ERROR", "Choose another resolution")
    else:
        audio.download(download_Folder)
        os.rename(os.path.join(download_Folder, audio_name_init), os.path.join(download_Folder, audio_name))
        video.download(download_Folder)

        # audio2 = ffmpeg.input(os.path.join(download_Folder, audio_name))
        # video2 = ffmpeg.input(os.path.join(download_Folder, video_name))
        # ffmpeg.output(audio2, video2, os.path.join(download_Folder, video_name)).run()
        # ffmpeg.concat(video2, audio2, v=1, a=1).output(os.path.join(download_Folder, video_name)).run()

        videoclip = VideoFileClip(os.path.join(download_Folder, video_name))
        audioclip = AudioFileClip(os.path.join(download_Folder, audio_name))
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        result_name = video_name+"_YouTube_Downloader.mp4"
        videoclip.write_videofile(os.path.join(download_Folder, result_name))

        os.remove(os.path.join(download_Folder, video_name))
        os.remove(os.path.join(download_Folder, audio_name))

        messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" + download_Folder)

    """
    try:
        video.download(download_Folder)
        getVideo.streams.filter(only_audio=True).first().download()
        messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" + download_Folder)
    except:
        messagebox.showinfo("ERROR", "Choose another resolution")
    """

def Download_audio():
    Youtube_link = video_Link.get()

    download_Folder = download_Path.get()

    getVideo = YouTube(Youtube_link)
    #videoStream = getVideo.streams.get_highest_resolution()
    audio = getVideo.streams.filter(only_audio=True).first()

    audio.download(download_Folder)

    out_file = audio.default_filename
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
   # os.path.join(download_Folder, out_file)
    os.rename(os.path.join(download_Folder, out_file), os.path.join(download_Folder, new_file))

    messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" + download_Folder)

# Creating object of tk class
root = tk.Tk()

# Setting the title, background color
# and size of the tkinter window and
# disabling the resizing property
root.geometry("600x400")
root.resizable(True, True)
root.title("YouTube Video And Audio Downloader")
root.config(background="gray")

# Creating the tkinter Variables
video_Link = StringVar()
download_Path = StringVar()
video_res = StringVar()

# Calling the Widgets() function
Widgets()

# Defining infinite loop to run
# application
root.mainloop()