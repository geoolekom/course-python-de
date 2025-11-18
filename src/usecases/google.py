from google import genai
from google.genai import types
import pandas as pd
import numpy as np

client = genai.Client()


def embed_article(
    article: pd.Series, chunk_size: int = 1000, overlap: int = 200
) -> pd.Series:
    text = article.md_text
    start = 0
    chunks: list[str] = []
    while start < len(article.md_text):
        end = start + chunk_size
        chunk = text[start:end]
        if end < len(text):
            last_period = chunk.rfind(".")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunks[:2],
        config=types.EmbedContentConfig(
            output_dimensionality=768, task_type="SEMANTIC_SIMILARITY"
        ),
    )
    embeddings = np.array(
        [np.array(embedding.values) for embedding in result.embeddings or []]
    )
    return pd.Series([embeddings], index=["embeddings"])


def embed_documents(df: pd.DataFrame) -> pd.DataFrame:
    df["embeddings"] = df.apply(embed_article, axis=1)
    return df
