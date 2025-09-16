import json
import pydantic

with open("data/data.json", "r") as f:
    d = json.load(f)


class FileComment(pydantic.BaseModel):
    user: str
    comment: str
    timestamp: str


class FileData(pydantic.BaseModel):
    title: str
    text: str
    author: str
    id: int
    tags: list[str]
    is_active: bool = False
    comments: list[FileComment] = pydantic.Field(default_factory=list)


class DataSchema(pydantic.BaseModel):
    files: list[FileData]


model = DataSchema(files=d["files"])
print(model)

for file in model.files:
    print(f"Title: {file.title}")
    print(f"Author: {file.author}")
    print(f"Tags: {', '.join(file.tags)}")
    print(f"Active: {file.is_active}")
    print("Comments:")
    for comment in file.comments:
        print(f" - {comment.user} said: {comment.comment} at {comment.timestamp}")

    print("-" * 40)
