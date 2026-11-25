from dataclasses import asdict
from pathlib import Path

from clean_code_lab.core import IdReport, report_ids
from clean_code_lab.policy import Proposal, RunContext, decide
from clean_code_lab.readers import make_reader


def baseline(expected_ids: list[str], observed_ids: list[str]) -> IdReport:
    """A deliberately wrong baseline for the lesson; never used by the core."""
    expected, observed = set(expected_ids), set(observed_ids)
    return IdReport(
        missing=sorted(expected - observed),
        unexpected=sorted(observed - expected),
        duplicates=[],
    )


def main() -> None:
    fixtures = Path(__file__).resolve().parents[1] / "fixtures"
    expected = make_reader("json").read(fixtures / "expected.json")
    observed = make_reader("csv").read(fixtures / "observed.csv")
    print("BASELINE:", asdict(baseline(expected, observed)))
    print("VERIFIED:", asdict(report_ids(expected, observed)))
    print("\nOFFLINE TOOL DECISIONS (no side effects)")
    proposals = (
        Proposal("read", "fixtures/observed.csv"),
        Proposal("run_check", "tests"),
        Proposal("write", "pyproject.toml"),
        Proposal("network", "remote endpoint"),
        Proposal("write", "../outside.txt"),
    )
    for index, proposal in enumerate(proposals):
        decision = decide(proposal, RunContext(actions_used=index))
        label = "PASS" if decision.allowed else "DENY"
        print(f"{label}  {proposal.action:10} {proposal.target:24} ({decision.reason})")


if __name__ == "__main__":
    main()
