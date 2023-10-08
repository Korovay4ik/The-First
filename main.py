import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, showwarning

root = Tk()
root.title("Database")
root.geometry("300x300+800+400")
root.resizable(False, False)
root.attributes("-toolwindow", True)

db = sqlite3.connect("database.db")
cur = db.cursor()


def register():
    log = login.get()
    cur.execute("SELECT COUNT(email) FROM users WHERE email = ?", (log,))
    item = cur.fetchone()[0]
    if len(log) > 12:
        showerror(title="Регистрация", message="Логин слишком длинный.")
    else:
        if login.get() != "" and item == 0:
            data = [login.get(), password.get()]
            cur.execute("INSERT INTO users VALUES (?,?)", data)
            db.commit()
            showinfo(title="Регистрация", message="Вы успешно зарегестрировались.")
        else:
            showerror(title="Регистрация", message="Данный логин уже занят.")


cur.execute("""CREATE TABLE IF NOT EXISTS users (
                                                email text,
                                                password text
                                                )""")


def vhod():
    log = login_entry.get()
    cur.execute("SELECT COUNT(email) FROM users WHERE email = ?", (log,))
    item = cur.fetchone()[0]
    if login.get() != "" and item == 0:
        showerror(title="Авторизация", message="Такого логина не существует.")
    else:
        cur.execute("SELECT password FROM users WHERE email = ?", (log,))
        pas = cur.fetchone()[0]
        if pas != password.get():
            showerror(title="Авторизация", message="Неверный пароль.")
        else:
            root.destroy()
            window = Tk()
            window.title("Вход")
            window.geometry("300x400+800+300")
            window.resizable(False, False)
            window.attributes("-toolwindow", True)
            label = ttk.Label(text="Вы успешно вошли!", foreground="#050505")
            label.pack(padx=0, pady=0, anchor=CENTER)
            chek_button = ttk.Button(text="База данных", command=chek)
            chek_button.pack(padx=5, pady=5, anchor=CENTER)


def chek():
    cur.execute("SELECT * FROM users")
    items = cur.fetchall()
    columns = ("Login", "Password")
    tree = ttk.Treeview(columns=columns, show="headings")
    tree.pack(fill=BOTH, expand=1)
    tree.heading("Login", text="Логин", anchor=W)
    tree.heading("Password", text="Пароль", anchor=W)
    tree.column("#1", stretch=NO, width=80)
    for user in items:
        tree.insert("", END, values=user)


db.commit()

label = ttk.Label(text="Логин: ")
label.place(x=45, y=5)
login = StringVar()
login_entry = ttk.Entry(textvariable=login, foreground="blue")
login_entry.pack(padx=5, pady=5, anchor=CENTER)

label = ttk.Label(text="Пароль: ")
label.place(x=37, y=35)
password = StringVar()
password_entry = ttk.Entry(textvariable=password, foreground="blue", show='♥')
password_entry.pack(padx=5, pady=5, anchor=CENTER)

reg_button = ttk.Button(text="Зарегистрироваться", command=register)
reg_button.pack(padx=5, pady=5, anchor=CENTER)

vhod_button = ttk.Button(text="Войти", command=vhod)
vhod_button.pack(padx=5, pady=5, anchor=CENTER)

root.mainloop()
