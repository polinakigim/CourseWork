import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from classes import PersonalBlog, Post, Comment, Tag

BLOGS_FILE = "data/blogs.json"

all_blogs = []
username = None
selected_blog = [None]


def save_blogs():
    with open(BLOGS_FILE, "w", encoding="utf-8") as f:
        json.dump([blog.to_dict() for blog in all_blogs], f, indent=2, ensure_ascii=False)


def load_blogs():
    if os.path.exists(BLOGS_FILE):
        with open(BLOGS_FILE, "r", encoding="utf-8") as f:
            return [PersonalBlog.from_dict(b) for b in json.load(f)]
    return []


def launch_main_app(user):
    global username, all_blogs
    username = user
    all_blogs = load_blogs()

    root = tk.Tk()
    root.title("Микроблог")

    left = tk.Frame(root)
    left.pack(side="left", fill="y")

    main = tk.Frame(root)
    main.pack(side="right", fill="both", expand=True)

    def logout():
        root.destroy()
        from auth import launch_auth_window
        launch_auth_window()

    def refresh_sidebar():
        for widget in left.winfo_children():
            widget.destroy()

        tk.Label(left, text=f"Вы: {username}", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(left, text="Лента", command=render_feed).pack(pady=15)

        for blog in all_blogs:
            if blog.owner == username:
                tk.Button(left, text=blog.name, width=20, command=lambda b=blog: show_blog(b)).pack(pady=2)

        tk.Button(left, text="Новый блог", command=create_blog).pack(pady=10)
        tk.Button(left, text="Выйти", command=logout).pack(pady=20)

    def create_blog():
        name = simpledialog.askstring("Название блога", "Введите название блога:")
        if name:
            blog = PersonalBlog(name, username)
            all_blogs.append(blog)
            save_blogs()
            refresh_sidebar()

    def add_post():
        blog = selected_blog[0]
        if blog and blog.owner != username:  # Проверка на None
            messagebox.showerror("Ошибка", "Вы не можете добавлять посты в чужой блог.")
            return

        title = simpledialog.askstring("Заголовок", "Введите заголовок:")
        content = simpledialog.askstring("Содержимое", "Введите текст поста:")
        tag_string = simpledialog.askstring("Теги", "Введите теги через запятую (например: еда,спорт):")
        tags = [Tag(tag.strip()) for tag in tag_string.split(",")] if tag_string else []

        if title and content:
            post = Post(title, content, username, tags)
            blog.posts.append(post)
            save_blogs()
            show_blog(blog)

    def toggle_like(post):
        if username in post.likes:
            post.likes.remove(username)
        else:
            post.likes.add(username)
        save_blogs()
        show_blog(selected_blog[0])

    def add_comment(post):
        text = simpledialog.askstring("Комментарий", "Введите текст:")
        if text:
            post.comments.append(Comment(username, text))
            save_blogs()
            show_blog(selected_blog[0])

    def show_blog(blog):
        if blog is None:  # Добавлена проверка на None
            return

        selected_blog[0] = blog
        for widget in main.winfo_children():
            widget.destroy()

        tk.Label(main, text=f"Блог: {blog.name}", font=("Arial", 14, "bold")).pack(pady=10)

        if blog.owner == username:
            tk.Button(main, text="Добавить пост", command=add_post).pack()

        for post in blog.posts:
            frame = tk.Frame(main, bd=1, relief="solid", padx=5, pady=5)
            frame.pack(fill="x", pady=5)

            formatted = post.content.replace("**", "").replace("*", "").replace("~~", "")
            tk.Label(frame, text=f"{post.title} ({post.author})", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(frame, text=formatted, wraplength=400).pack(anchor="w")

            if post.tags:
                tag_str = " ".join(str(tag) for tag in post.tags)
                tk.Label(frame, text=f"Теги: {tag_str}", fg="blue").pack(anchor="w")

            tk.Button(frame, text=f"❤{len(post.likes)}", command=lambda p=post: toggle_like(p)).pack(anchor="w")
            tk.Button(frame, text="Комментировать", command=lambda p=post: add_comment(p)).pack(anchor="w")

            for comment in post.comments:
                tk.Label(frame, text=f"{comment.author}: {comment.text}", fg="gray").pack(anchor="w", padx=10)

    def render_feed():
        for widget in main.winfo_children():
            widget.destroy()

        tk.Label(main, text="Все посты", font=("Arial", 14)).pack(pady=10)

        for blog in all_blogs:
            for post in blog.posts:
                frame = tk.Frame(main, bd=1, relief="solid", padx=5, pady=5)
                frame.pack(fill="x", pady=5)

                tk.Label(frame, text=f"{post.title} ({post.author})", font=("Arial", 12, "bold")).pack(anchor="w")
                tk.Label(frame, text=post.content, wraplength=400).pack(anchor="w")

                if post.tags:
                    tag_str = " ".join(str(tag) for tag in post.tags)
                    tk.Label(frame, text=f"Теги: {tag_str}", fg="blue").pack(anchor="w")

                tk.Button(frame, text=f"❤{len(post.likes)}", command=lambda p=post: toggle_like(p)).pack(anchor="w")
                tk.Button(frame, text="Комментировать", command=lambda p=post: add_comment(p)).pack(anchor="w")
                tk.Button(frame, text="Перейти к блогу", command=lambda b=blog: show_blog(b)).pack(anchor="w")

    refresh_sidebar()
    render_feed()
    root.mainloop()
