from async_s3 import __version__
from async_s3.main import as3
from click.testing import CliRunner


def test_version():
    assert __version__


def test_version_option():
    runner = CliRunner()
    result = runner.invoke(as3, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output
