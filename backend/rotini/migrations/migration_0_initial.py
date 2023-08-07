"""
Generated: 2023-08-07T16:14:11.314059

Message: Files table initial migration
"""
UID = "06f02980-864d-4832-a894-2e9d2543a79a"

PARENT = "None"

MESSAGE = "Files table initial migration"

UP_SQL = """CREATE TABLE
    files
(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    path text NOT NULL,
    size bigint NOT NULL
);
"""
DOWN_SQL = """DROP TABLE files;"""
