from models.mongo import ScientificArticle
import storage.mongo  # noqa: F401


def list_articles() -> list[ScientificArticle]:
    return ScientificArticle.objects.all()  # type: ignore[no-any-return]


if __name__ == "__main__":
    print(list_articles())
