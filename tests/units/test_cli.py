from tempyenv.cli import TemporaryVenvCreator
import tempfile
import unittest
import sys
import os


class TestCli(unittest.TestCase):

    def test_basic_init(self):
        cli = TemporaryVenvCreator()
        assert(cli.temp_dir == None)
        assert(cli.venv_path == None)

    def test_create_temporary_directory(self):
        cli = TemporaryVenvCreator()
        cli.create_temporary_directory()
        assert(cli.temp_dir != None)
        assert(cli.venv_path != None)

    def test_python_exec(self):
        cli = TemporaryVenvCreator(python_exec="python_test")
        assert(cli.python_exec == "python_test")
