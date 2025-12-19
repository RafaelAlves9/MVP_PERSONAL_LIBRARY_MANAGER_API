import requests


class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org"
    DEFAULT_TIMEOUT = 10

    @classmethod
    def search(cls, *, author: str | None = None, title: str | None = None, query: str | None = None, page: int = 1, limit: int = 10) -> dict:
        params = {"page": page, "limit": limit}
        if author:
            params["author"] = author
        if title:
            params["title"] = title
        if query:
            params["q"] = query

        response = requests.get(f"{cls.BASE_URL}/search.json", params=params, timeout=cls.DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()

    @classmethod
    def fetch_work(cls, work_key: str) -> dict | None:
        # work_key vem no formato "/works/OLxxxxW"
        normalized = work_key.lstrip("/")
        response = requests.get(f"{cls.BASE_URL}/{normalized}.json", timeout=cls.DEFAULT_TIMEOUT)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

