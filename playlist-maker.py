import os
import urllib.request
import re
from tkinter import *


def execute():
    global file_name, playlist_name

    file_name = file_name.get()
    playlist_name = playlist_name.get()

    file = open(f'{file_name}', 'rt')

    os.system(f'mkdir "/Users/korbi/Desktop/{playlist_name}"')

    for line in file:
        video_url = 'https://www.youtube.com/watch?v='
        line_info = line.split('-')
        song_artist = line_info[0].rstrip(' ').replace(' ', '+')
        song_title = line_info[1].rstrip('\n').lstrip(' ').replace(' ', '+')
        search_url = f'https://www.youtube.com/results?search_query={song_artist}+-+{song_title}'

        html_content = urllib.request.urlopen(search_url)
        results = re.findall('/watch\?v=(.{11})', html_content.read().decode())

        if len(results) > 0:
            video_url = video_url + results[0]
            os.system(f'youtube-dl --extract-audio --audio-format mp3 {video_url} -o "/Users/korbi/Desktop/{playlist_name}/{song_artist.replace("+", " ")} - {song_title.replace("+", " ")}.%(ext)s" ')

    text_done = Text(window, highlightthickness=0, height=1, bg='#90EE90')
    text_done.insert(INSERT, 'Done making playlist')
    text_done.pack()


window = Tk(className='Playlist Creator')

checkVar = IntVar()
newFVar = IntVar()
existing = Checkbutton(window, text='Existing file', variable=checkVar)
newF = Checkbutton(window, text='New file', variable=newFVar)

file_name = StringVar()
playlist_name = StringVar()

labelFile = Label(window, text='File name: ')
labelFile.pack()

entry = Entry(window, textvariable=file_name, width=33)
entry.pack()

labelMix = Label(window, text='Playlist name: ')
labelMix.pack()

entry = Entry(window, textvariable=playlist_name, width=33)
entry.pack()

frame = Frame(window)
frame.pack()

button = Button(frame, text='Go', command=execute)
close = Button(frame, text='Exit', command=window.destroy)
button.grid(row=0, column=0)
close.grid(row=0, column=1)

text = Text(window, highlightthickness=0, height=10)
text.insert(INSERT, 'Directions: \n1. Write down names of songs in a .txt file with the following format:[ARTIST_NAME] - [SONG_TITLE]\n2. Enter the name of your playlist \n3. Press Go!')
text.pack()

window.mainloop()
