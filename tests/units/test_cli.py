from tempyenv.cli import TemporaryVenvCreator
import unittest


class TestCli(unittest.TestCase):

    def test_basic_init(self):
        cli = TemporaryVenvCreator()
        assert(cli.temp_dir is None)
        assert(cli.venv_path is None)

    def test_create_temporary_directory(self):
        cli = TemporaryVenvCreator()
        cli.create_temporary_directory()
        assert(cli.temp_dir is not None)
        assert(cli.venv_path is not None)

    def test_python_exec(self):
        cli = TemporaryVenvCreator(python_exec="python_test")
        assert(cli.python_exec == "python_test")
