"""
Generated: 2023-08-19T23:04:28.163820

Message: None
"""
UID = "141faa0b-6868-4d07-a24b-b45f98d2809d"

PARENT = "06f02980-864d-4832-a894-2e9d2543a79a"

MESSAGE = "Creates the user table."

UP_SQL = """CREATE TABLE
    users
(
    id bigserial PRIMARY KEY,
    username varchar(64) NOT NULL,
    password_hash varchar(128) NOT NULL,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    password_updated_at timestamp DEFAULT now(),
    CONSTRAINT unique_username UNIQUE(username)
)
"""

DOWN_SQL = """DROP TABLE users;"""
