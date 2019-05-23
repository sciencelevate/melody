import os
from tkinter import *
import tkinter.messagebox
from pygame import mixer
from tkinter import filedialog
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
import time

playPath = []

def show_details(play_song):

    file_data = os.path.splitext(play_song)
    if file_data[1] == 'mp3':
        audio = MP3(play_song)
        totalLength = audio.info.length
    else:
        a = mixer.Sound(play_song)
        totalLength = a.get_length()
    #divmod divides the value by 60, quotient is in mins and remainder in secs
    mins, secs = divmod(totalLength, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = 'Total length'+' - '+ timeformat

    bThread = threading.Thread(target=thread_function, args=(totalLength,))
    bThread.start()


def thread_function(t):
    global paused
    Current_time = 0
    while Current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(Current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimeLabel['text'] = "Current Time" + " - " + timeformat
            time.sleep(1)
            Current_time = Current_time+1

def play_music():
    global paused
    paused = False
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music resumed"+"  "+ os.path.basename(filename_path)
        paused = False
    else:
        try:
                stop_music()
                time.sleep(1)
                selected_song = playList.curselection()
                selected_song = int(selected_song[0])
                play_it = playPath[selected_song]
                mixer.music.load(play_it)
                mixer.music.play()
                statusbar['text'] = "Playing music" +"  "+ os.path.basename(play_it)
                show_details(play_it)
        except:
                tkinter.messagebox.showerror("File not found", "Please select a music file")

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music stopped"

def set_vol(val):
    volume = float(val) / 100 #As the mixer only takes values in the range of 0 to 1
    mixer.music.set_volume(volume) #volume uses the float value

def about_us():
    tkinter.messagebox.showinfo("Credits", "This was made by Sitakanta")

#It contains the full path + filename
#playlistbox contains the filename
#Full path is to play the music using load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    index = 0
    playPath.insert(index, filename)
    filename = os.path.splitext(filename)
    playList.insert(index, filename)
    index += 1

def del_song():
    selected_song = playList.curselection()
    selected_song = int(selected_song[0])
    playList.delete(selected_song)
    del playPath[selected_song]
    print(playPath)

def set_scale():
    scale.set(50)
    mixer.music.set_volume(0.5)

def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music paused"

def rewind_music():
    try:
        mixer.music.load(filename_path)
        mixer.music.play()
        statusbar['text'] = "music rewinded" + "  " + os.path.basename(filename_path)
    except:
        tkinter.messagebox.showerror("There is no music selected, yet", "Please select a music file using open from the file menu")

def mute_music():
    global muted
    muted = False
    if muted:
        #unmute the music
        scale.set(50)
        mixer.music.set_volume(0.5)
        volume_button.configure(image=volumePhoto)
        muted = False

    else:
        volume_button.configure(image=mutePhoto)
        scale.set(0)
        mixer.music.set_volume(0)
        muted = True

def on_closing():
    stop_music()
    root.destroy()

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

#created the menu bar

menubar = Menu(root)
root.config(menu=menubar)

statusbar = Label(root, text="Welcome to melody", relief=SUNKEN, anchor=W, font ="Times 12 bold")
statusbar.pack(side=BOTTOM, fill=X)

#Started mixer from

mixer.init()

root.title("Melody")
root.iconbitmap(r'images/melody.ico')

#created the submenu

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="file", menu=subMenu)
subMenu.add_command(label="Open", command = browse_file)
subMenu.add_command(label="Exit", command= root.destroy)

#creates another submenu

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About", command=about_us)

#Root Window = StatusBar, LeftFrame, RightFrame
#LeftFrame = The listbox (playlist)
#RightFrame = TopFrame, MiddleFrame and the bottomFrame

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx= 30)

playList = Listbox(leftframe)
playList.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)

delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

middleframe = Frame(rightframe, relief=RAISED)
middleframe.pack(padx=10, pady=10)

bottonframe = Frame(rightframe)
bottonframe.pack(padx=10, pady=30)

lengthLabel = ttk.Label(topframe, text="Total length = --:--", font="verdana 8 bold")
lengthLabel.pack(pady=10)

currenttimeLabel = ttk.Label(topframe, text="Current time = --:--", relief=GROOVE, font="verdana 8")
currenttimeLabel.pack(pady=10)

playPhoto = PhotoImage(file="images/play.png")
play_button = ttk.Button(middleframe, image=playPhoto, command= play_music)
play_button.grid(row=0, column=0, padx=5)

stopPhoto = PhotoImage(file="images/stop.png")
stop_button = ttk.Button(middleframe, image=stopPhoto,  command=stop_music)
stop_button.grid(row=0, column= 1, padx=5)

pausePhoto = PhotoImage(file="images/pause.png")
pause_button = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pause_button.grid(row=0, column=2, padx=5)

rewindPhoto = PhotoImage(file="images/rewind.png")
rewind_button = ttk.Button(bottonframe, image=rewindPhoto, command=rewind_music)
rewind_button.grid(row=0, column=0, padx=10)

mutePhoto = PhotoImage(file="images/mute.png")
volumePhoto = PhotoImage(file='images/speaker.png')
volume_button = ttk.Button(bottonframe, image=volumePhoto, command= mute_music)
volume_button.grid(row=0, column=1)

scale = ttk.Scale(bottonframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
set_scale()
scale.grid(row=0, column=2)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

root.mainloop()