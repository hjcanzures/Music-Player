from tkinter import *
from tkinter import messagebox
import requests
import pygame
import io
import urllib.request
import tempfile
import os

def dashboard_page():
    window = Tk()
    window.title("Dashboard")
    window.geometry("925x500+300+200")
    window.configure(bg="#eb84eb")

    # Initialize pygame mixer
    pygame.mixer.init()

    # Header
    header = Frame(window, bg='orchid', height=80)
    header.pack(fill="x")
    Label(header, text="BeatVerse Dashboard", fg="white", bg="orchid",
          font=("Arial Black", 28, "bold")).pack(pady=10)

    # Main frame
    frame = Frame(window, bg="orchid")
    frame.pack(pady=10)

    Label(frame, text="Welcome to your Dashboard!",
          fg="white", bg="orchid",
          font=("Segoe UI", 18, "bold")).pack(pady=10)

    music_listbox = Listbox(frame, width=60, height=10, font=("Segoe UI", 12))
    music_listbox.pack(pady=10)

    music_urls = {}           # Map listbox index -> music URL
    current_temp_file = None  # Store path to current temp file

    # Fetch music from API
    def fetch_music():
        try:
            response = requests.get("http://127.0.0.1:5000/api/music")
            music_data = response.json()
            music_listbox.delete(0, END)
            music_urls.clear()
            for idx, song in enumerate(music_data):
                music_listbox.insert(END, f"{song['title']} - {song['artist']}")
                music_urls[idx] = song['url']
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch music: {e}")

    # Stop current music and delete temp file if exists
    def stop_current_music():
        nonlocal current_temp_file
        pygame.mixer.music.stop()
        if current_temp_file and os.path.exists(current_temp_file):
            try:
                os.remove(current_temp_file)
            except PermissionError:
                pass  # sometimes the OS locks file briefly

    # Play selected song
    def play_music(event=None):
        nonlocal current_temp_file
        try:
            index = music_listbox.curselection()[0]
            url = music_urls[index]

            stop_current_music()  # Stop previous song

            # Create temp file for new song
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                data = urllib.request.urlopen(url).read()
                tmp.write(data)
                current_temp_file = tmp.name

            pygame.mixer.music.load(current_temp_file)
            pygame.mixer.music.play()

            messagebox.showinfo("Now Playing", f"Playing: {music_listbox.get(index)}")

        except IndexError:
            messagebox.showwarning("Select Song", "Please select a song to play!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not play music: {e}")

    # Buttons frame (horizontal layout)
    button_frame = Frame(frame, bg="orchid")
    button_frame.pack(pady=10)

    Button(button_frame, text="Load Music", width=20, height=2,
           bg='blue violet', fg='white',
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           cursor='hand2', command=fetch_music).grid(row=0, column=0, padx=5)

    Button(button_frame, text="Play Selected", width=20, height=2,
           bg='blue violet', fg='white',
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           cursor='hand2', command=play_music).grid(row=0, column=1, padx=5)

    Button(button_frame, text="Stop", width=20, height=2,
           bg='red', fg='white',
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           cursor='hand2', command=stop_current_music).grid(row=0, column=2, padx=5)

    Button(button_frame, text="Logout", width=20, height=2,
           bg='blue violet', fg='white',
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           cursor='hand2', command=window.destroy).grid(row=0, column=3, padx=5)

    # Double-click to play
    music_listbox.bind("<Double-1>", play_music)

    window.mainloop()


if __name__ == "__main__":
    dashboard_page()
