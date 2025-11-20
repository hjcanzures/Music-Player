from tkinter import *
from tkinter import messagebox
import sqlite3
import signin
import bcrypt


def signup_page():
    global window, user, code, confirm_code

    window = Tk()
    window.title('Sign Up')
    window.geometry('925x500+300+200')
    window.configure(bg="#eb84eb")

    frame = Frame(window, width=350, height=430, bg='orchid',
                  highlightbackground="black", highlightthickness=2)
    frame.pack(pady=50)

    # tITLEe
    Label(frame, text='Sign up\nfor exclusive music!', fg='white', bg='orchid',
          font=('Arial Black', 20, 'bold')).place(relx=0.5, y=20, anchor='n')


    # USERNAME
    def user_enter(e):
        if user.get() == "Username":
            user.delete(0, END)

    def user_leave(e):
        if user.get() == "":
            user.insert(0, "Username")

    user = Entry(frame, width=25, fg="white", border=0, bg="orchid",
                 font=('Microsoft YaHei UI Light', 11, 'bold'))
    user.place(x=30, y=120)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', user_enter)
    user.bind('<FocusOut>', user_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=147)

    # PASSWORD
    def pass_enter(e):
        code.delete(0, END)
        code.config(show="*")

    def pass_leave(e):
        if code.get() == "":
            code.insert(0, 'Password')
            code.config(show="")

    code = Entry(frame, width=25, fg='white', border=0, bg="orchid",
                 font=('Microsoft YaHei UI Light', 11, 'bold'))
    code.place(x=30, y=180)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', pass_enter)
    code.bind('<FocusOut>', pass_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=207)

    # CONFIRM PASSWORD
    def confirm_enter(e):
        confirm_code.delete(0, END)
        confirm_code.config(show="*")

    def confirm_leave(e):
        if confirm_code.get() == "":
            confirm_code.insert(0, 'Confirm Password')
            confirm_code.config(show="")

    confirm_code = Entry(frame, width=25, fg='white', border=0, bg="orchid",
                         font=('Microsoft YaHei UI Light', 11, 'bold'))
    confirm_code.place(x=30, y=240)
    confirm_code.insert(0, 'Confirm Password')
    confirm_code.bind('<FocusIn>', confirm_enter)
    confirm_code.bind('<FocusOut>', confirm_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=267)

    def register_user():
        username = user.get()
        password = code.get()
        confirm = confirm_code.get()

        if username == "Username" or password == "Password":
            messagebox.showerror("Error", "Please fill all fields")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save to database
        conn = sqlite3.connect("users_beat.db")
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )""")

        try:
            cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()

            messagebox.showinfo("Success", "Account created successfully!")
            window.destroy()
            signin.signin_page()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

        finally:
            conn.close()

    # SIGNUP BUTTON
    Button(frame, width=28, pady=7, text='Sign up', bg='blue violet', fg='white',
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           cursor='hand2', border=0,
           command=register_user).place(x=30,y=300)


    Label(frame, text="I have an account.", fg="black", bg='orchid',
          font=('Microsoft YaHei UI Light', 11, 'bold')).place(x=60, y=360)

    Button(frame, width=6, text="Login ", border=0, bg='orchid',
           font=('Microsoft YaHei UI Light', 11, 'bold'),
           cursor='hand2', fg='white',
           command=lambda: [window.destroy(), signin.signin_page()]).place(x=210, y=360)

    window.mainloop()


if __name__ == "__main__":
    signup_page()
