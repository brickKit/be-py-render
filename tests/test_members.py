"""What is installed, at which version, is exactly what component.yaml declares (the pitfall "the shell's member
list, the compiled members and the lock disagree"), and the shell's own version is the manifest's."""
import pathlib

import yaml

from be_py_render import VERSION, members

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_members_match_the_manifest():
    m = yaml.safe_load((ROOT / "component.yaml").read_text())
    declared = sorted(m["shell"]["members"])
    installed = sorted(f"{d.id}@{d.version}" for d in members())
    assert declared and declared == installed
    assert m["metadata"]["version"] == VERSION
    project = (ROOT / "pyproject.toml").read_text()
    assert f'version = "{VERSION}"' in project


def test_the_launcher_accepts_the_members_it_compiles():
    # the launcher's own refusals about what is installed, run on this environment: a member's distribution at another
    # version than its manifest (the Python probe stayed at 3.2.20 through 3.2.25) or an SDK it does not meet (P1.21)
    # would otherwise show only when a deployment hosts that member
    import json

    from besdk import shell

    defs = members()
    served = json.dumps([{"componentId": d.id, "version": d.version, "httpPort": 9000 + i} for i, d in enumerate(defs)])
    _, refusals, warnings = shell.check(served, defs, shell.installed_of, False)
    install = [r for r in refusals if r.key.endswith((":componentId", ":version", ":distribution", ":be-sdk"))]
    assert install == [] and warnings == []
