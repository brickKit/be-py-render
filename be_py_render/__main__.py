"""Runs the shell (the image's entry point)."""
from be_py_render import identity, members
from besdk import shell

shell.main(identity(), *members())
