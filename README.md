# postgresql-for-novices

[Documentation](https://project-c-sql.github.io/)

## Notes for developers

### Poetry

This project uses [Poetry](https://python-poetry.org/) for packaging. Although one should refer to [Poetry docs](https://python-poetry.org/docs/) for a thorough introduction, here's a short summary of the intended workflow with Poetry:

- To install all dependencies and the application, type `poetry install`. After installation, if the Python scripts folder is in your PATH, you should be able to invoke `main.main()` with `pg4n`.
- To make VS Code use Poetry's virtual environment, type `poetry env info`, copy virtual environment executable path, press F1 and type `Python: Select Interpreter` > `Enter interpreter path...` > paste path and press `<ENTER>`.
- To add/remove a dependency, type `poetry add <dep>`/`poetry remove <dep>`.
- To execute a command from within virtual environment shell, type `poetry run <cmd>`.
- To enter a shell session within the Poetry virtual environment, type `poetry shell`.

### Imports

During development, you must run the program as a module, e.g., `poetry run python -m src.pg4n.main`, so that the imports work.

### Running tests

Having PostgreSQL running on port 5432, do `poetry run pytest`.

You may need to provide environment variables that match your config:

| Variable     | Default value   | Description                                             |
| ------------ | --------------- | ------------------------------------------------------- |
| `PGHOST`     | `127.0.0.1`     | Hostname of the PostgreSQL server.                      |
| `PGPORT`     | `5432`          | Port to an active PostgreSQL instance.                  |
| `PGUSER`     | `postgres`      | The user that will be used to manage the test database. |
| `PGPASSWORD` |                 | Password, in case password authentication is used.      |
| `PGDBNAME`   | `test_database` | Database name.                                          |
 
For example, if PostgreSQL is on port 5433, just do `PGPORT=5433 poetry run pytest` (Bash syntax).

#### Using docker

To get a similar PostgreSQL instance as with GitHub Actions workflow:<br>
`docker run --rm -P -p 127.0.0.1:5432:5432 --name pg -e POSTGRES_PASSWORD=postgres -d postgres:14.5-alpine`

You'll need to tell pytest the password: `PGPASSWORD=postgres poetry run pytest`.

### Building documents

1. If `docs/api` is not up-to-date or doesn't exist, run:<br>`poetry run sphinx-apidoc -f -o docs/api src/pg4n '*/test_*'`
2. To generate the documentation:<br>`poetry run sphinx-build -b html docs docs/build`

Note that the GitHub Pages site is only updated on pushes to `main` branch.

<!-- TODO: generate appropriately scoped access token so a bot can comment lint results
### Linting

For linting, you need the CI tools: `poetry install -with ci`.

Running all linters:
```
poetry run '
mypy src --show-error-codes --show-error-context --pretty &&
black src --check &&
isort "src"/**/*.py -m 3 --trailing-comma -c &&
pylint src'
```
-->
