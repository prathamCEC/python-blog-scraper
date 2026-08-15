import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL = "https://blog.python.org/"

HEADERS = {
    "User-Agent": "curl/8.5.0"
}


def scrape_posts():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("article.post-card")

    print(f"Found {len(articles)} articles")

    posts = []

    for article in articles:

        title_element = article.select_one("h3")
        date_element = article.select_one("time")
        summary_element = article.select_one("p")

        if not title_element:
            continue

        title = title_element.get_text(
            " ",
            strip=True
        )

        published_date = (
            date_element.get("datetime")
            if date_element
            else None
        )

        author_element = (
            date_element.find_previous("span")
            if date_element
            else None
        )

        author = (
            author_element.get_text(strip=True)
            if author_element
            else "Unknown"
        )

        summary = (
            summary_element.get_text(
                " ",
                strip=True
            )
            if summary_element
            else ""
        )

        link_element = title_element.find_parent("a")

        if not link_element:
            continue

        url = urljoin(
            URL,
            link_element.get("href")
        )

        post = {
            "title": title,
            "author": author,
            "published_date": published_date,
            "summary": summary,
            "url": url
        }

        posts.append(post)

    return posts


if __name__ == "__main__":

    posts = scrape_posts()

    for post in posts:
        print(post)
        print("-" * 80)
