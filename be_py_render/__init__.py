"""The Python render shell: one process hosting the members installed in its environment, each on its own port with
its own runtime (be-sdk-python's shell launcher). Which members it hosts in a deployment is BrickKit's choice
(BRICKKIT_SERVED_MEMBERS_CONFIG); the launcher refuses members that are not installed or not at the declared
version."""
from besdk.component import Definition
from besdk.shell import Identity

ID, VERSION = "be/py-render", "3.0.20"


def members() -> list[Definition]:
    """The definitions installed in this shell, at the versions uv.lock pins (by tag); they must equal shell.members in
    component.yaml (tests/test_members.py)."""
    import infra_print
    import probe_py

    return [*probe_py.definitions(), infra_print.definition()]  # the experiment's probes and infra/print


def identity() -> Identity:
    return Identity(ID, VERSION)
