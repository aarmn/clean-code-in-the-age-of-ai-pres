from clean_code_lab.core import IdReport, report_ids
from clean_code_lab.demo import baseline


def test_report_keeps_all_three_kinds_of_findings() -> None:
    assert report_ids(["January", "February"], ["January", "March", "January"]) == IdReport(
        missing=["February"],
        unexpected=["March"],
        duplicates=["January"],
    )


def test_duplicate_results_are_unique_and_sorted() -> None:
    assert report_ids([], ["z", "a", "z", "a", "a"]).duplicates == ["a", "z"]


def test_all_collections_can_be_empty() -> None:
    assert report_ids([], []) == IdReport(missing=[], unexpected=[], duplicates=[])


def test_acceptance_fixture_catches_deliberately_bad_baseline() -> None:
    expected, observed = ["January"], ["January", "January"]
    assert baseline(expected, observed) != report_ids(expected, observed)
