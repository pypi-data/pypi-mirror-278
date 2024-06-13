from sqlalchemy_utils import create_database, database_exists, drop_database


def reset_database(db_url: str) -> None:
    if database_exists(db_url):
        drop_database(db_url)

    create_database(db_url)

    print(f"Database reset: {db_url}")
