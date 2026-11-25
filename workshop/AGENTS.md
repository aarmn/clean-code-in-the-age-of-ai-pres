# Booking workshop

- Run the checks below from this project directory.
- Put booking rules in `booking/domain.py`. Keep FastAPI request handling and HTTP status mapping in `booking/api.py`.
- Add tests for behavior changes. Preserve existing HTTP responses unless the task explicitly changes them.
- Ask before adding dependencies. The exercise uses synthetic data.

```sh
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy booking tests
uv run --locked pytest -q
```
