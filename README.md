# Clean Code In the AI Age

A 90-minute Slidev workshop for developers who already know Python, presented by Alireza (Aryan) Mohammadnejad at Shahid Beheshti University.

**Live slides:** https://clean-code-in-the-age-of-ai-pres.vercel.app

1. **Clean Code: Classic** (60 min). Concepts that work in any language first: readability, with an incremental refactor that adds one concept per step; principles (KISS, DRY, YAGNI and each SOLID letter with a code example, Liskov's original definition, when principles collide, and Design by Contract); code smells, including Gall's law, value types with operator overloading, and Literal vs Enum; design patterns (Factory, Strategy, Adapter, classic and Pythonic Singleton, Dependency Injection, Service Locator); and structure (MVC and Django's MTV, three-layer architecture, where business logic lives, GRASP). Then Python: PEPs and the full Zen of Python, dataclasses, Pydantic, docstrings (styles, and building HTML docs with pdoc, Sphinx or MkDocs), logging, and a Protocol detour; a tour of Python features to learn (built-ins, map, f-strings, lru_cache, copy and deepcopy, pickle, decorators, typing); and tooling (Ruff, mypy, uv, pytest). Then beyond the code: OpenAPI and observability. A "skip to the resources" link on the part-one recap jumps past part two when time runs short.
2. **Clean Code: Age of AI** (30 min). Instructions (task briefs, AGENTS.md, skills, MCP), tools and permissions, choosing a model, and reviewing what an agent wrote.

One running project, a seat-booking API, carries every example. Each chapter opens with a title page; each topic fixes a real problem in the project and ends with one piece of advice.

## Run it

Node.js 22 or newer and [pnpm](https://pnpm.io/).

```sh
pnpm install
pnpm run dev      # opens http://localhost:3030
pnpm run build    # static site in dist/
```

Fonts (Fraunces, Open Sans, DejaVu Mono) are bundled from npm, so the deck renders the same offline. Book covers on the last slide load from Open Library and fall back to a text cover when offline.

## Files

- `slides.md`: the slides and their speaker notes.
- `style.css`: the visual system. `components/`: the 3D dot sphere, QR codes and book cards. `global-top.vue`: the footer, which reads `part` and `chapter` from each slide's frontmatter.
- `PRESENTER.md`: run of show with timings. `SPEAKER-NOTES.md`: every slide's notes. Both are generated from `slides.md`.
- `workshop/`: the seat-booking API used in the slides, with tests, `AGENTS.md`, and the cancellation exercise with a reference patch. See its README.
- `demo/`: an earlier report-reconciliation lab, kept for reference; the current slides don't use it.

## Deploy

Vercel builds the site from `vercel.json` (`pnpm run build`, output `dist/`). The build uses hash routing, so `dist/` also works from any static file server.

## Reading and references

- Books on the last slide: [Clean Code](https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884), [Refactoring](https://martinfowler.com/books/refactoring.html), [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php), [Fluent Python](https://www.fluentpython.com/), [Architecture Patterns with Python](https://www.cosmicpython.com/) (free online), [AI Engineering](https://github.com/chiphuyen/aie-book), [Python Notes for Professionals](https://books.goalkicker.com/PythonBook/) (free PDF).
- Python PEPs: [8 · style](https://peps.python.org/pep-0008/), [20 · the Zen of Python](https://peps.python.org/pep-0020/), [257 · docstrings](https://peps.python.org/pep-0257/), [484 · type hints](https://peps.python.org/pep-0484/), [572 · assignment expressions](https://peps.python.org/pep-0572/), [585 · generic built-ins](https://peps.python.org/pep-0585/), [604 · unions](https://peps.python.org/pep-0604/), [649](https://peps.python.org/pep-0649/) and [749 · annotation semantics](https://peps.python.org/pep-0749/), [695 · type aliases](https://peps.python.org/pep-0695/).
- Tooling: [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [mypy](https://mypy.readthedocs.io/en/stable/), [Pyright](https://github.com/microsoft/pyright), [ty](https://docs.astral.sh/ty/), [Pyrefly](https://pyrefly.org/).
- [OpenAPI](https://spec.openapis.org/oas/v3.1.2.html), [FastAPI](https://fastapi.tiangolo.com/features/), [Sentry Python SDK](https://docs.sentry.io/platforms/python/), [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/).
- [AGENTS.md](https://agents.md/), [Agent Skills spec](https://agentskills.io/specification), [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture).
- [Hugging Face Models Hub](https://huggingface.co/docs/hub/models-the-hub), [Ollama](https://docs.ollama.com/), [llama.cpp](https://github.com/ggml-org/llama.cpp), [Langfuse](https://langfuse.com/docs/observability/overview).
- [Aryan’s portfolio and talks](https://aarmn.com/).

The examples use synthetic data. The model evaluation table contains illustrative figures, not measured vendor comparisons.
