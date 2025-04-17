import json
from abc import ABC, abstractmethod


# Классы для Пользователей
class AbstractUser(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass

    @abstractmethod
    def get_role(self):
        pass


class User(AbstractUser):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = "user"

    def to_dict(self):
        return {"username": self.username, "password": self.password, "role": self.role}

    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"], data["password"])
        user.role = data.get("role", "user")
        return user

    def get_role(self):
        return self.role


# Классы для Блогов
class AbstractBlog(ABC):
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.posts = []

    @abstractmethod
    def add_post(self, title, content, author):
        """Метод для добавления поста в блог"""
        pass

    @abstractmethod
    def get_blog_info(self):
        """Метод для получения основной информации о блоге"""
        pass

    def get_posts(self):
        """Возвращает список всех постов в блоге"""
        return self.posts

    def to_dict(self):
        """Метод для сериализации блога в словарь"""
        return {
            "name": self.name,
            "owner": self.owner,
            "posts": [post.to_dict() for post in self.posts],
        }

    @classmethod
    def from_dict(cls, data):
        """Метод для десериализации блога из словаря"""
        blog = cls(data["name"], data["owner"])
        blog.posts = [Post.from_dict(p) for p in data.get("posts", [])]
        return blog


class PersonalBlog(AbstractBlog):
    def __init__(self, name, owner):
        super().__init__(name, owner)

    def add_post(self, title, content, author):
        if author == self.owner:
            self.posts.append(Post(title, content, author))

    def get_blog_info(self):
        return f"Personal Blog: {self.name} by {self.owner}"


class Comment:
    def __init__(self, author, text):
        self.author = author
        self.text = text

    def to_dict(self):
        return {"author": self.author, "text": self.text}

    @classmethod
    def from_dict(cls, data):
        return cls(data["author"], data["text"])


class Post:
    def __init__(self, title, content, author, tags=None):
        self.title = title
        self.content = content
        self.author = author
        self.comments = []
        self.likes = set()
        self.tags = tags or []

    def add_like(self, user):
        """Добавить лайк пользователю"""
        if user.username not in self.likes:
            self.likes.add(user.username)

    def remove_like(self, user):
        """Удалить лайк пользователя"""
        if user.username in self.likes:
            self.likes.remove(user.username)

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "comments": [c.to_dict() for c in self.comments],
            "likes": list(self.likes),
            "tags": [tag.to_dict() for tag in self.tags]
        }

    @classmethod
    def from_dict(cls, data):
        post = cls(data["title"], data["content"], data["author"])
        post.comments = [Comment.from_dict(c) for c in data.get("comments", [])]
        post.likes = set(data.get("likes", []))
        post.tags = [Tag.from_dict(t) for t in data.get("tags", [])]
        return post

class Tag:
    def __init__(self, name):
        self.name = name.lower().strip()

    def to_dict(self):
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"])

    def __str__(self):
        return f"#{self.name}"

    def __eq__(self, other):
        return isinstance(other, Tag) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

