from clean_code_lab.policy import Proposal, RunContext, decide


def test_allows_known_check_and_fixture() -> None:
    assert decide(Proposal("run_check", "tests"), RunContext()).allowed
    assert decide(Proposal("read", "fixtures/observed.csv"), RunContext()).allowed


def test_denies_out_of_scope_paths_and_unknown_checks() -> None:
    assert not decide(Proposal("write", "pyproject.toml"), RunContext()).allowed
    assert not decide(Proposal("write", "../outside.txt"), RunContext()).allowed
    assert not decide(Proposal("run_check", "unknown"), RunContext()).allowed


def test_does_not_grant_network_or_publishing() -> None:
    assert not decide(Proposal("network", "external"), RunContext()).allowed
    assert not decide(Proposal("publish", "repository"), RunContext()).allowed


def test_disabled_checks_or_exhausted_budget_deny_action() -> None:
    assert not decide(
        Proposal("run_check", "tests"), RunContext(can_run_checks=False)
    ).allowed
    assert not decide(Proposal("run_check", "tests"), RunContext(actions_used=10)).allowed
