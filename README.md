# rotini
An unnamed cloud storage app

## Development

### Tooling

Utility commands are managed by [go-task](https://github.com/go-task/task) and can be called from anywhere. Running `.
script/bootstrap` installs `go-task` within the project and gets everything ready. From there, `task -l` provides a
breakdown of available tools.

Note that this is the preferred way to running any tooling-related task within the repository, regardless of
environment.

### Running locally

The application requires a Postgres database instance to be made available to the backend. This can be done for you via
`task be:start-db`.

Starting the backend and frontend applications can be done via `task be:start` and `task fe:start`.

See the README files of each of those environments ([backend](./backend/README.md), [frontend](./frontend/README.md)) for specific requirements (i.e. environment dotfiles).
