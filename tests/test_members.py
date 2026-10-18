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
