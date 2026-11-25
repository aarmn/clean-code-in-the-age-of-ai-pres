# Local Python teaching lab

A deterministic synthetic demo. No LLM, network action, shell execution by the policy, or HTTP service. `openapi.yaml` is a complete example contract for a potential HTTP wrapper, not a server included here.

```sh
uv sync --locked
uv run --offline python -m clean_code_lab.demo
uv run --offline ruff format --check .
uv run --offline ruff check .
uv run --offline mypy clean_code_lab tests
uv run --offline pytest -q
```

The stdlib-only demo also works with `python -m clean_code_lab.demo` from this folder. `policy.py` illustrates how to decide whether an action would be allowed. It does not isolate code. Real enforcement needs a sandbox/worker policy outside the model, credential management, audit logs, and verified path handling.
