from tkinter import *
from tkinter import messagebox
import ast
import sqlite3
import signup
import dboard
import bcrypt


def signin_page():
    global window, user, code

    window = Tk()
    window.title('Login')
    window.geometry('925x500+300+200')
    window.configure(bg="#eb84eb")

    frame = Frame(window, width=350, height=390, bg='orchid', highlightbackground="black", highlightthickness=2)
    frame.pack(pady=70)


    Label(frame, text='Login', fg='white', bg='orchid',
          font=('Arial Black', 28, 'bold')).place(x=120, y=5)


    def on_enter(e): user.delete(0, 'end')
    def on_leave(e):
        if user.get() == '':
            user.insert(0, 'Username')

    user = Entry(frame, width=25, fg="white", border=0, bg="orchid",
                 font=('Microsoft YaHei UI Light', 11, 'bold'))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)


    def pass_enter(e):
        code.delete(0, 'end')
        code.config(show='*')

    def pass_leave(e):
        if code.get() == '':
            code.insert(0, 'Password')
            code.config(show='')

    code = Entry(frame, width=25, fg="white", border=0, bg="orchid",
                 font=('Microsoft YaHei UI Light', 11, 'bold'))
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', pass_enter)
    code.bind('<FocusOut>', pass_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    def signin():
        username = user.get()
        password = code.get()

        conn = sqlite3.connect("users_beat.db")
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            messagebox.showinfo("Login", "Login Successful!")
            window.destroy()
            dboard.dashboard_page()
        else:
            messagebox.showerror("Invalid", "Invalid Username or Password")

        conn.close()



    Button(frame, width=28, pady=7, text='Login', bg='blue violet', fg='white',
           font=('Microsoft YaHei UI Light', 11, 'bold'),
            border=0, command=signin).place(x=30, y=220)

    Label(frame, text="Don't have an account?", fg="black", bg='orchid',
            font=('Microsoft YaHei UI Light', 11, 'bold')).place(x=30, y=315)

    Button(frame, width=6, text="Sign up", border=0, bg='orchid', cursor='hand2',
           font=('Microsoft YaHei UI Light', 11, 'bold'),
            fg='white', command=lambda: [window.destroy(), signup.signup_page()]).place(x=225, y=315)

    frame.pack()
    window.mainloop()


if __name__ == "__main__":
    signin_page()
