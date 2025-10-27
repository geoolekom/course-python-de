import csv
from pathlib import Path

from sqlalchemy.exc import IntegrityError

from models.relational import ScientificArticle, Author
from storage.relational_db import Session


def load_data_from_csv(path: Path) -> None:
    with open(path, "r") as f:
        reader = csv.DictReader(f, delimiter=";")
        for line in reader:
            with Session() as session:
                try:
                    author = Author(
                        full_name=line["author_full_name"], title=line["author_title"]
                    )
                    article = ScientificArticle(
                        title=line["title"],
                        summary=line["summary"],
                        file_path=line["file_path"],
                        arxiv_id=line["arxiv_id"],
                        author=author,
                    )
                    session.add(article)
                    session.commit()
                    print(f"Success: {article.arxiv_id}")
                except IntegrityError as e:
                    print(f"Failure: {e}")


if __name__ == "__main__":
    load_data_from_csv(Path("data/articles.csv"))
