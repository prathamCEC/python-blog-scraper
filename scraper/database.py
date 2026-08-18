import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def insert_posts(posts):

    connection = get_connection()

    inserted_count = 0

    try:
        with connection.cursor() as cursor:

            for post in posts:

                cursor.execute(
                    """
                    INSERT INTO blog_posts (
                        title,
                        author,
                        published_date,
                        summary,
                        url,
                        scraped_at
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (url) DO NOTHING
                    """,
                    (
                        post["title"],
                        post["author"],
                        post["published_date"],
                        post["summary"],
                        post["url"],
                        post["scraped_at"]
                    )
                )

                inserted_count += cursor.rowcount

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return inserted_count
