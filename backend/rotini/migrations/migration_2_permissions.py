"""
Generated: 2023-08-27T11:56:17.800102

Message: Sets up permission-tracking on files
"""
UID = "3c755dd8-e02d-4a29-b4ee-2afa4d9b30d6"

PARENT = "141faa0b-6868-4d07-a24b-b45f98d2809d"

MESSAGE = "Sets up permission-tracking on files"

UP_SQL = """CREATE TABLE
    permissions_files
(
    id bigserial PRIMARY KEY,
    file_id uuid NOT NULL,
    user_id bigint NOT NULL,
    value bigint NOT NULL,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    CONSTRAINT file_fk FOREIGN KEY(file_id) REFERENCES files(id),
    CONSTRAINT user_fk FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT unique_permission_per_file_per_user UNIQUE(file_id, user_id)
);
"""

DOWN_SQL = """DROP TABLE permissions_files;"""
