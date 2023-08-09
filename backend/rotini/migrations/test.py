"""
Creates the initial files table.
"""

UP_SQL = """CREATE TABLE
    files
(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    path text NOT NULL,
    size bigint NOT NULL
);
"""

DOWN_SQL = """
DROP TABLE files
"""
