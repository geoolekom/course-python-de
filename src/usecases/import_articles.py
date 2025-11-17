from sqlalchemy.exc import IntegrityError

from models.relational import ScientificArticle, Author
from storage.relational_db import Session
import pandas as pd

pd.set_option("display.max_columns", None)


def save_article(line: pd.Series) -> pd.Series:
    with Session() as session:
        try:
            author = Author(
                full_name=line["author_full_name"], title=line["author_title"]
            )
            article = ScientificArticle(
                title=line["title"],
                summary=line["summary"][:500],
                file_path=line["file_path"],
                arxiv_id=line["arxiv_id"],
                author=author,
            )
            session.add(article)
            session.commit()
            session.refresh(article)
            # print(f"Success: {article.arxiv_id}")
            return pd.Series([article.id, author.id], index=["db_id", "author_db_id"])
        except IntegrityError:
            # print(f"Failure: {e}")
            return pd.Series([0, 0], index=["db_id", "author_db_id"])


def create_in_relational_db(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(save_article, axis=1)
    df = pd.concat([df, ids], axis=1)
    return df
