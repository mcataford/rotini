import psycopg2

from settings import settings


def get_connection():
    """
    Create a database connection.
    """
    return psycopg2.connect(
        user=settings.DATABASE_USERNAME,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_NAME,
    )
