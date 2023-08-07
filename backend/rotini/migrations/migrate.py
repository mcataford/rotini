"""
Migration handler.

This module handles database migrations.

Migrations are expected to be Python files of the format:

```
UID = <UUID, current migration>

PARENT = <UUID, migration that must be applied before present>

MESSAGE = <str, message>

UP_SQL = <SQL>

DOWN_SQL = <SQL>
```

where UP_SQL is the change the migration represents and DOWN_SQL its inverse.

Usage:

python migrate.py <up|down|new> [<migration_name, if new>]

Not including a migration name executes everything from the last executed
migration.
"""

import os
import collections
import pathlib
import datetime
import uuid
import typing
import importlib
import sys

import psycopg2

VALID_COMMANDS = ["up", "down", "new"]

DIRECTION_UP = 1
DIRECTION_DOWN = -1

# UUID attached to a migration.
MigrationID = str

# Filename (without ext.) of a migration.
MigrationModuleName = str

MigrationItem = collections.namedtuple("MigrationItem", "id module")


def _get_connection():
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


def _ensure_migration_table():
    """
    Ensure that the migration tracking table exists.
    """
    connection = _get_connection()

    maybe_create_sql = """
    CREATE TABLE IF NOT EXISTS migrations_lastapplied (
        migration_uid text NOT NULL
    );
    """

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(maybe_create_sql)


def _get_migration_sequence() -> typing.List[MigrationItem]:
    """
    Collects migration files and builds a historical
    timeline.

    This will detect duplicates and breaks in the sequence
    and raise if the history is not linear and complete.
    """
    migrations_dir = pathlib.Path(".")
    migrations: typing.Dict[MigrationID, MigrationModuleName] = {}
    dependency_map: typing.Dict[MigrationID, MigrationID] = {}

    for file in migrations_dir.iterdir():
        if file.name.startswith("migration_") and file.suffix == ".py":
            migration = importlib.import_module(file.stem)
            migration_id = migration.UID
            migration_parent = migration.PARENT

            if migration_id in migrations:
                raise RuntimeError("Duplicate migrations.")

            if migration_parent in dependency_map:
                raise RuntimeError("History must be linear.")

            migrations[migration_id] = str(file.stem)
            dependency_map[migration_parent] = migration_id

    if not dependency_map:
        print("No migrations yet!")
        return []

    root_id = dependency_map["None"]
    history: typing.List[MigrationItem] = [MigrationItem(root_id, migrations[root_id])]

    while history:
        next_id = dependency_map.get(history[-1].id)

        if next_id is None:
            break

        history.append(MigrationItem(next_id, migrations[next_id]))

    return history


def migrate(direction: typing.Union[typing.Literal[1], typing.Literal[-1]]):
    """
    Runs a migration (expected to be in the current directory
    and labeled 'migration_<label>.py'.
    """
    _ensure_migration_table()

    connection = _get_connection()
    full_history, applied_migrations = _get_migration_sequence(), []
    last_applied = None

    with connection, connection.cursor() as cursor:
        cursor.execute('SELECT migration_uid FROM "migrations_lastapplied"')
        last_applied_row = cursor.fetchone()
        last_applied = last_applied_row[0] if last_applied_row else None

    full_history_ids = [migration.id for migration in full_history]

    if last_applied is not None and last_applied not in full_history_ids:
        raise RuntimeError("Last applied migration is not in history.")

    for migration_item in full_history:
        if last_applied is None:
            break

        applied_migrations.append(migration_item)

        if last_applied is not None and migration_item.id == last_applied:
            break

    migrations_to_apply = (
        full_history[len(applied_migrations) :]
        if direction == DIRECTION_UP
        else list(reversed(applied_migrations))
    )

    collected_sql = []
    for migration_item in migrations_to_apply:
        migration = importlib.import_module(migration_item.module)
        migration_sql = (
            migration.UP_SQL if direction == DIRECTION_UP else migration.DOWN_SQL
        )
        collected_sql.append(migration_sql)
        print(f"Collected {migration_item.module}: {migration.MESSAGE}")

    with connection, connection.cursor() as cursor:
        for pos, sql in enumerate(collected_sql):
            print(f"Applying {migrations_to_apply[pos][1]}")
            cursor.execute(sql)

        next_last_applied = (
            None if direction == DIRECTION_DOWN else migrations_to_apply[-1].id
        )

        if next_last_applied is None:
            cursor.execute("DELETE FROM migrations_lastapplied;")
        elif last_applied is None:
            cursor.execute(
                "INSERT INTO migrations_lastapplied (migration_uid) VALUES (%s);",
                (next_last_applied,),
            )
        else:
            cursor.execute(
                "UPDATE migrations_lastapplied SET migration_uid = %s",
                (next_last_applied,),
            )


def create_migration_file(label: str, message: typing.Optional[str]):
    """
    Create a new migration file with with a dependency on the last migration
    in history.
    """
    migration_seq = _get_migration_sequence()

    print("Found migrations:")
    for migration_id, migration_file in migration_seq:
        print(f"{migration_id}: {migration_file}")

    parent_uid = migration_seq[-1][0] if migration_seq else None

    migration_uid = str(uuid.uuid4())
    now = datetime.datetime.now().isoformat()
    content = f"""\"\"\"
Generated: {now}

Message: {message}
\"\"\"
UID = "{migration_uid}"

PARENT = "{parent_uid}"

MESSAGE = "{message}"

UP_SQL = \"\"\" \"\"\"

DOWN_SQL = \"\"\" \"\"\"
"""

    migration_filename = f"migration_{len(migration_seq)}_{label}.py"

    with open(migration_filename, "w", encoding="utf8") as migration_file:
        migration_file.write(content)

    print(f"Created {migration_filename}.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError("Supply up/down as a first argument.")
    if sys.argv[1] not in VALID_COMMANDS:
        raise RuntimeError("Invalid commands.")

    arguments = sys.argv[1:]

    COMMAND = arguments[0]
    MIGRATION_NAME = arguments[1] if len(arguments) >= 2 else None
    MIGRATION_MESSAGE = arguments[2] if len(arguments) == 3 else None

    if COMMAND == "up":
        migrate(DIRECTION_UP)
    elif COMMAND == "down":
        migrate(DIRECTION_DOWN)
    elif COMMAND == "new":
        create_migration_file(MIGRATION_NAME, MIGRATION_MESSAGE)
