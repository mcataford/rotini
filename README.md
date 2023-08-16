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

#### Starting the backend application

The backend application is available as a container, which you can run as

```sh
task be:start
```

If you opt to run your database in an adjacent container, you can either run containers in such a manner than they share
a network or define the database's host via `docker.host.internal`:

```sh
task be:start -- --add-host docker.host.internal:host-gateway
```

More generally, extra options can be passed to the `docker run` call that runs the application this way:

```sh
task be:start -- <options>
```

See the README files of each of those environments ([backend](./backend/README.md), [frontend](./frontend/README.md)) for specific requirements..
