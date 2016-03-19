from directory_tools.directory_tools import DirectoryTools


def test_return_code() -> None:
    application = DirectoryTools([])
    assert application.run() == 0
