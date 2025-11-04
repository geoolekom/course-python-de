import pymupdf4llm
from models.mongo import ScientificArticle as MongoArticle, Author as MongoAuthor
import storage.mongo  # noqa: F401
from mongoengine import DoesNotExist
import pandas as pd


def save_article(article: pd.Series) -> pd.Series:
    try:
        m_author = MongoAuthor(
            db_id=article.author_db_id,
            full_name=article.author_full_name,
            title=article.author_title,
        )
        md_text = pymupdf4llm.to_markdown(article.file_path)
        kwargs = dict(
            db_id=article.db_id,
            title=article.title,
            summary=article.summary,
            file_path=article.file_path,
            arxiv_id=article.arxiv_id,
            author=m_author,
            text=md_text,
        )
        try:
            m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
            m_article.update(**kwargs)
        except DoesNotExist:
            m_article = MongoArticle(**kwargs)
            m_article.save()

        print(f"Success: {article.arxiv_id}")
        mongo_db_id: str = str(m_article.id)
        return pd.Series([mongo_db_id], index=["mongo_db_id"])
    except Exception as e:
        print(f"Failure: {e}")
        return pd.Series([""], index=["mongo_db_id"])


def create_in_mongo(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(save_article, axis=1)
    df = pd.concat([df, ids], axis=1)
    return df
