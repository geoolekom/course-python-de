import io
import requests
import pandas as pd


url = "http://export.arxiv.org/api/query"


def fetch_arxiv_articles(query: str, i: int = 0) -> pd.DataFrame:
    params: dict[str, str | int] = {
        "search_query": f"all:{query}",
        "start": i,
        "max_results": 10,
    }
    response = requests.get(url, params=params)
    xml_data = response.text
    return load_from_xml(xml_data)


def load_from_xml(xml_data: str) -> pd.DataFrame:
    file_like = io.StringIO(xml_data)
    df = pd.read_xml(
        file_like,
        xpath="/atom:feed/atom:entry",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )[["id", "title", "summary"]]

    df["author_title"] = "PhD"

    file_like = io.StringIO(xml_data)

    links_df = pd.read_xml(
        file_like,
        xpath="/atom:feed/atom:entry/atom:link[@title='pdf']",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )["href"]

    file_like = io.StringIO(xml_data)

    authors_df = pd.read_xml(
        file_like,
        xpath="/atom:feed/atom:entry/atom:author[1]",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )["name"]

    return pd.concat(
        [
            df.rename(columns={"id": "arxiv_id"}),
            links_df.rename("file_path"),
            authors_df.rename("author_full_name"),
        ],
        axis=1,
    )
