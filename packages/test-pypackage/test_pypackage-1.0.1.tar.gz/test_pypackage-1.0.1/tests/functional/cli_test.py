from subprocess import run


def test_help():
    """Test the test-pypackage --help command."""
    run(["test-pypackage", "--help"], check=True)


def test_version():
    """Test the test-pypackage --version command."""
    run(["test-pypackage", "--version"], check=True)
