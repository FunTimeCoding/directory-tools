from directory_tools.directory_tools import DirectoryTools


def test_return_code():
    application = DirectoryTools([])
    assert application.run() == 0
