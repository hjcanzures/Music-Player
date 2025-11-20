from tkinter import *
from tkinter import messagebox
from tkinter import font
import signin
import signup


def home_page():

    global window, mylogo

    window = Tk()
    window.title('Home Page')
    window.geometry('925x500+300+200')
    window.configure(bg="#eb84eb")

    # Header
    header = Frame(window, bg='orchid', height=80)
    header.pack(fill="x")

    # Logo
    mylogo = PhotoImage(file="beat_logo.png")
    mylogo = mylogo.subsample(5, 5)

    Label(header, text="BeatVerse", fg="white", bg="orchid",
          image=mylogo, compound="left",
          font=('Arial Black', 28, 'bold')).pack(side="left", padx=20)


    def signup_link():
        window.destroy()
        signup.signup_page()

    def signin_link():
        window.destroy()
        signin.signin_page()

    btn_frame = Frame(header, bg="orchid")
    btn_frame.pack(side="right", padx=20)

    Button(btn_frame, text="Login", width=12, height = 2, cursor='hand2',
           bg='blue violet', fg='white', border=0,
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           command=signin_link).pack(side="left", padx=10)

    Button(btn_frame, text="Sign Up", width=12, height = 2, cursor='hand2',
           bg='blue violet', fg='white', border=0,
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           command=signup_link).pack(side="left", padx=10)

    # Main Frame
    frame = Frame(window, width=800, height=350, bg='orchid')
    frame.pack(pady=40)


    # App Title
    Label(frame, text='BeatVerse', fg='white', bg='orchid',
          font=('Arial Black', 36, 'bold')).pack(pady=10, padx=150)

    # Description
    Label(frame, text='Play your favorite tracks \nRight where you are',
          fg='white', bg='orchid',
          font=('Segoe UI', 16, 'bold')).pack(pady=10)

    # Play Music button
    Button(frame, width=18, height=2, text='Play Music', cursor='hand2',
           bg='blue violet', fg='white', border=0,
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           command=signup_link).pack(pady=20)



    window.mainloop()


if __name__ == "__main__":
    home_page()

