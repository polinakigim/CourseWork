from classes import User
from app import launch_main_app
import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "data/users.json"


def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return {u["username"]: User.from_dict(u) for u in json.load(f)}


def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([user.to_dict() for user in users.values()], f, indent=2, ensure_ascii=False)


def launch_auth_window():
    users = load_users()

    root = tk.Tk()
    root.title("Авторизация")

    def login():
        username = entry_user.get()
        password = entry_pass.get()
        user = users.get(username)
        if user and user.password == password:
            root.destroy()
            launch_main_app(username)
        else:
            messagebox.showerror("Ошибка", "Неверные данные")

    def register():
        username = entry_user.get()
        password = entry_pass.get()
        if username in users:
            messagebox.showerror("Ошибка", "Пользователь уже существует")
        else:
            users[username] = User(username, password)
            save_users(users)
            messagebox.showinfo("Успешно", "Регистрация завершена")

    root.geometry("300x200")
    tk.Label(root, text="ВХОД В СИСТЕМУ").pack()

    tk.Label(root, text="Логин:").pack()
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Пароль:").pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    tk.Button(root, text="Войти", command=login).pack(pady=5)
    tk.Button(root, text="Зарегистрироваться", command=register).pack()

    root.mainloop()
