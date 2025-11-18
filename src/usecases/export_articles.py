from pathlib import Path
import pymupdf4llm
from urllib.parse import urlparse

import requests
from models.mongo import ScientificArticle as MongoArticle, Author as MongoAuthor
import storage.mongo  # noqa: F401
from mongoengine import DoesNotExist
import pandas as pd


def download_file(article: pd.Series) -> pd.Series:
    parsed_url = urlparse(article.file_path)
    if parsed_url.scheme:
        filename = Path(parsed_url.path).name
        new_path = f"data/articles/{filename}.pdf"
        if not Path(new_path).exists():
            response = requests.get(article.file_path)
            with open(new_path, "wb") as f:
                f.write(response.content)
    else:
        new_path = article.file_path

    return pd.Series([new_path], index=["local_file_path"])


def convert_article_to_markdown(article: pd.Series) -> pd.Series:
    md_text = pymupdf4llm.to_markdown(article.local_file_path)
    with open(f"{article.local_file_path}.md", "w") as f:
        f.write(md_text)
    return pd.Series([md_text], index=["md_text"], dtype="string")


def save_article(article: pd.Series) -> pd.Series:
    try:
        m_author = MongoAuthor(
            db_id=article.author_db_id,
            full_name=article.author_full_name,
            title=article.author_title,
        )
        kwargs = dict(
            db_id=article.db_id,
            title=article.title,
            summary=article.summary,
            file_path=article.file_path,
            arxiv_id=article.arxiv_id,
            author=m_author,
            text=article.md_text,
        )
        try:
            m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
            m_article.update(**kwargs)
        except DoesNotExist:
            m_article = MongoArticle(**kwargs)
            m_article.save()

        mongo_db_id: str = str(m_article.id)
        return pd.Series([mongo_db_id], index=["mongo_db_id"])
    except Exception:
        return pd.Series([""], index=["mongo_db_id"])


def create_in_mongo(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(save_article, axis=1)
    df = pd.concat([df, ids], axis=1)
    return df


def download_files(df: pd.DataFrame) -> pd.DataFrame:
    filenames = df.apply(download_file, axis=1)
    df = pd.concat([df, filenames], axis=1)
    return df


def convert_to_markdown(df: pd.DataFrame) -> pd.DataFrame:
    texts = df.apply(convert_article_to_markdown, axis=1)
    df = pd.concat([df, texts], axis=1)
    return df
