# Seat-booking workshop

This small FastAPI project accompanies the **Clean Code in the AI Age** talk. Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run the commands from this folder.

```sh
uv sync --locked
uv run --locked uvicorn booking.api:app --reload
```

Use the Swagger UI at [localhost:8000/docs](http://127.0.0.1:8000/docs) to create a booking for two seats with ID `A42`. Try again to see HTTP 409. The schema is at [localhost:8000/openapi.json](http://127.0.0.1:8000/openapi.json). The teaching store lives in one process, resets on restart, and does not enforce uniqueness across concurrent requests or workers.

## Run the checks

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy booking tests
uv run --locked pytest -q
```

To compare Astral’s checker on the same files, run `uv run --locked ty check booking tests`. This repo uses mypy as its primary check.

## Pair exercise

Give an agent, or your partner, this task.

> Add `DELETE /bookings/{booking_id}`. An active booking can be cancelled and returns 204 with an empty body. Repeating that cancellation returns 204 with an empty body. An ID that never existed returns 404. Preserve existing `POST` behavior and avoid new dependencies. Update the OpenAPI response declarations and add tests.

Review the patch for behavior, scope, and whether it follows `AGENTS.md`. Run the checks. Inspect the generated OpenAPI responses for `DELETE`.

## Try the reference solution

From a clean copy of this folder, preview and apply the bundled patch.

```sh
git apply --check cancellation-reference.patch
git apply cancellation-reference.patch
uv run --locked pytest -q
```

The reference implementation keeps the booking ID and stores a cancellation flag. The existing create endpoint still returns its original public fields. A cancelled ID continues to be reserved, so a later `POST` of the same ID returns 409.
