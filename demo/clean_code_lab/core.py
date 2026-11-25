from collections import Counter
from dataclasses import dataclass


@dataclass
class IdReport:
    missing: list[str]
    unexpected: list[str]
    duplicates: list[str]


def report_ids(expected_ids: list[str], observed_ids: list[str]) -> IdReport:
    expected, observed = set(expected_ids), set(observed_ids)
    counts = Counter(observed_ids)
    return IdReport(
        missing=sorted(expected - observed),
        unexpected=sorted(observed - expected),
        duplicates=sorted(k for k, count in counts.items() if count > 1),
    )
