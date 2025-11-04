from usecases.import_articles import create_in_relational_db, load_data_from_csv
from usecases.export_articles import create_in_mongo
from usecases.search_text import search_text_index

if __name__ == "__main__":
    df = (
        load_data_from_csv("data/articles.csv")
        .pipe(create_in_relational_db)
        .pipe(create_in_mongo)
    )
    print("DataFrame after relational DB insertion:")
    print(df)

    results = search_text_index("Hubble tension")
    print("len results:", len(results))
    for article in results:
        print(f"{article.arxiv_id}: {article.title}")
