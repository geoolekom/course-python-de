from usecases.embed import chunk_documents, embed_documents
from usecases.import_articles import create_in_relational_db
from usecases.export_articles import (
    convert_to_markdown,
    download_files,
)
from usecases.search_text import search_text_index
from usecases.arxiv import fetch_arxiv_articles

from tqdm.auto import tqdm

from usecases.vector import check_chunks_in_qdrant

tqdm.pandas(desc="Loading articles")

if __name__ == "__main__":
    df = (
        fetch_arxiv_articles("proton")
        .pipe(create_in_relational_db)
        .pipe(download_files)
        .pipe(convert_to_markdown)
        .pipe(chunk_documents)
        .pipe(check_chunks_in_qdrant)
        .pipe(embed_documents)
        # .pipe(save_to_qdrant)
        # .pipe(create_in_mongo)
    )
    print("DataFrame after relational DB insertion:")
    print(df)

    results = search_text_index("angular")
    print("len results:", len(results))
    for article in results:
        print(f"{article.arxiv_id}: {article.title}")
