import json
import typing as t

with open("data/data.json", "r") as f:
    d = json.load(f)


class FileComment(t.TypedDict):
    user: str
    comment: str
    timestamp: str


class FileData(t.TypedDict):
    title: str
    text: str
    author: str
    id: int
    tags: list[str]
    is_active: t.NotRequired[bool]
    comments: t.NotRequired[list[FileComment]]


data: list[FileData] = d["files"]
for file in data:
    print(f"Title: {file['title']}")
    print(f"Author: {file['author']}")
    print(f"Tags: {', '.join(file['tags'])}")
    print(f"Active: {file['is_active']}")
    print("Comments:")
    for comment in file["comments"]:
        print(
            f" - {comment['user']} said: {comment['comment']} at {comment['timestamp']}"
        )
    print("-" * 40)
