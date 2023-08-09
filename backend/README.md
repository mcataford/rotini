# Rotini backend

## Development

Before starting, make sure to run the [root bootstrap script](../README.md#Development) so the `task` commands are enabled.

Locally, a Postgres database that can be used for development can be started via `docker-compose up -d`.

An envfile should be present at `.env` and should define:

- `DATABASE_USERNAME`, the username to initialize the DB user with;
- `DATABASE_PASSWORD`, the password to assign to that test user;
- `DATABASE_HOST`, the host on which the database runs;
- `DATABASE_PORT`, the port on which the database runs;
- `DATABASE_NAME`, name of the database within the Postgres instance.

