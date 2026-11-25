# Presenter run of show

90 minutes, no reserved Q&A. Part 01 (Classic) runs to minute 60; part 02 (Age of AI) runs 60–90. Open **Presenter Mode** from the lower-left Slidev toolbar for notes and the next-slide preview; `SPEAKER-NOTES.md` has the same notes.

_Generated from the speaker notes in `slides.md`._

| # | Minutes | Part · chapter | Slide |
|---:|:---|:---|:---|
| 1 | 0–1 | Opening | Clean Code In the AI Age |
| 2 | 1–3 | Opening | Why listen to me? |
| 3 | 3–4 | Opening | From knowing Python to using it well |
| 4 | 4–5 | 01 · Classic · Why clean code | Clean Code: Classic |
| 5 | 5–7 | 01 · Classic · Why clean code | Clean code answers three questions |
| 6 | 7–9 | 01 · Classic · The project | A seat-booking API for this workshop |
| 7 | 9–10 | 01 · Classic · The project | Concepts first. Python second. |
| 8 | 10–14 | 01 · Classic · Readability | Version 0 works. Can you change it? |
| 9 | 14–15 | 01 · Classic · Readability | Name things after the problem, not the code |
| 10 | 15–17 | 01 · Classic · Principles | KISS, DRY, YAGNI in the booking API |
| 11 | 17–20 | 01 · Classic · Principles | SOLID, one booking example per letter |
| 12 | 20–21 | 01 · Classic · Principles | Ask “what will change?” before “which principle?” |
| 13 | 21–23 | 01 · Classic · Design patterns | Factory: decide once, at the edge |
| 14 | 23–25 | 01 · Classic · Design patterns | Strategy: swap the pricing rule, keep the service |
| 15 | 25–27 | 01 · Classic · Design patterns | Adapter: our code speaks Booking, not Stripe |
| 16 | 27–29 | 01 · Classic · Design patterns | Singleton: one Settings object, passed in |
| 17 | 29–30 | 01 · Classic · Design patterns | Learn patterns as vocabulary, not as goals |
| 18 | 30–33 | 01 · Classic · Structure | Where does each piece live? MVC, MVVM, GRASP |
| 19 | 33–34 | 01 · Classic · Structure | Start with a function. Add a layer when change asks for it. |
| 20 | 34–36 | 01 · Classic · Python | Python wrote its principles down: the PEPs |
| 21 | 36–38 | 01 · Classic · Python | Give your data a shape: dataclass and Enum |
| 22 | 38–40 | 01 · Classic · Python | Small built-ins that delete whole bugs |
| 23 | 40–41 | 01 · Classic · Python | Learn your language’s standard library |
| 24 | 41–43 | 01 · Classic · Python | Know which Python you’re writing |
| 25 | 43–44 | 01 · Classic · Python | Pick a Python version on purpose, then use all of it |
| 26 | 44–46 | 01 · Classic · Tooling | Three checks, three different jobs |
| 27 | 46–48 | 01 · Classic · Tooling | Rebuild the same environment with one command |
| 28 | 48–49 | 01 · Classic · Tooling | Pick one type checker and make it a gate |
| 29 | 49–51 | 01 · Classic · Tooling | Tests: rules written as examples |
| 30 | 51–52 | 01 · Classic · Tooling | Let machines nitpick, so humans can review the design |
| 31 | 52–54 | 01 · Classic · Beyond the code | OpenAPI: a contract clients can depend on |
| 32 | 54–56 | 01 · Classic · Beyond the code | Observability: let production tell you what broke |
| 33 | 56–57 | 01 · Classic · Beyond the code | Make the system explain itself |
| 34 | 57–60 | 01 · Classic · Beyond the code | Where our booking API ended up |
| 35 | 60–61 | 02 · Age of AI · Instructions | Clean Code: Age of AI |
| 36 | 61–64 | 02 · Age of AI · Instructions | Ask for an outcome that can be checked |
| 37 | 64–66 | 02 · Age of AI · Instructions | Write the project guide once: AGENTS.md |
| 38 | 66–68 | 02 · Age of AI · Instructions | A skill saves a recipe you repeat |
| 39 | 68–70 | 02 · Age of AI · Instructions | MCP: one plug for tools and context |
| 40 | 70–71 | 02 · Age of AI · Instructions | Onboard your agent like a new teammate |
| 41 | 71–73 | 02 · Age of AI · Tools & permissions | A tool needs a narrow shape and a gate |
| 42 | 73–75 | 02 · Age of AI · Tools & permissions | Decide permissions before the run |
| 43 | 75–76 | 02 · Age of AI · Tools & permissions | Enforce limits in the harness, not in the prompt |
| 44 | 76–78 | 02 · Age of AI · Choosing a model | How to find a good model for your case |
| 45 | 78–80 | 02 · Age of AI · Choosing a model | Twenty booking tasks, three candidates |
| 46 | 80–81 | 02 · Age of AI · Choosing a model | Your test suite is your benchmark |
| 47 | 81–84 | 02 · Age of AI · Review | Demo · An agent adds cancellation |
| 48 | 84–86 | 02 · Age of AI · Review | Review the evidence, then merge |
| 49 | 86–88 | 02 · Age of AI · Review | Your first hour back at the keyboard |
| 50 | 88–89 | 02 · Age of AI · Review | Make it readable. Make it checkable. |
| 51 | 89–90 | 02 · Age of AI · Resources | Six books worth your next year |

## Demo cues

1. Slides 8, 36 and 41 are click-throughs: each click changes the code and swaps the list beside it.
2. Before the talk, open a terminal in `workshop/` and run `uv sync --locked` once.
3. On the demo slide, give the task from `workshop/README.md` to an agent, or apply `cancellation-reference.patch` if there is no time or network. Then run `uv run --locked pytest -q` and open `/docs` to show the DELETE responses.
