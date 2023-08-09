import os

import psycopg2


def get_connection():
    """
    Create a database connection.
    """
    return psycopg2.connect(
        user=os.environ["DATABASE_USERNAME"],
        password=os.environ["DATABASE_PASSWORD"],
        host=os.environ["DATABASE_HOST"],
        port=os.environ["DATABASE_PORT"],
        database=os.environ["DATABASE_NAME"],
    )
