from usecases.import_articles import create_in_relational_db, load_from_xml
from usecases.export_articles import create_in_mongo, download_files
from usecases.search_text import search_text_index

if __name__ == "__main__":
    df = (
        load_from_xml("data/arxiv_articles.xml")
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
