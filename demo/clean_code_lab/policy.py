"""Offline decisions only. No shell, filesystem writes, or network execution."""

from dataclasses import dataclass
from typing import Literal

_CHECKS = frozenset({"lint", "types", "tests"})
_SHARED_FIXTURES = frozenset({"fixtures/observed.csv", "fixtures/expected.json"})
_DRAFT_PATHS = frozenset({"clean_code_lab/core.py", "tests/test_core.py"})
Action = Literal["read", "write", "run_check", "network", "publish"]


@dataclass(frozen=True)
class Proposal:
    action: Action
    target: str


@dataclass(frozen=True)
class RunContext:
    can_run_checks: bool = True
    actions_used: int = 0
    action_limit: int = 10


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def decide(proposal: Proposal, run: RunContext) -> Decision:
    if run.actions_used >= run.action_limit:
        return Decision(False, "action limit")
    match proposal:
        case Proposal("read", target) if target in _SHARED_FIXTURES | _DRAFT_PATHS:
            return Decision(True, "listed path")
        case Proposal("write", target) if target in _DRAFT_PATHS:
            return Decision(True, "listed draft path")
        case Proposal("run_check", target) if run.can_run_checks and target in _CHECKS:
            return Decision(True, "listed check")
        case Proposal("read" | "write", _):
            return Decision(False, "out of scope")
        case _:
            return Decision(False, "disabled or unrecognized")
