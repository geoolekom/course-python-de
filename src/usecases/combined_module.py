from usecases.import_articles import create_in_relational_db
from usecases.export_articles import create_in_mongo, download_files
from usecases.search_text import search_text_index
from usecases.arxiv import fetch_arxiv_articles

if __name__ == "__main__":
    df = (
        fetch_arxiv_articles("proton")
        .pipe(create_in_relational_db)
        .pipe(download_files)
        .pipe(create_in_mongo)
    )
    print("DataFrame after relational DB insertion:")
    print(df)

    results = search_text_index("angular")
    print("len results:", len(results))
    for article in results:
        print(f"{article.arxiv_id}: {article.title}")
