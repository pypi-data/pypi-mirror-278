from unittest.mock import Mock, patch


RK = 'wizlib.ui.shell.line_editor.readkey'


def mock_keys(keys: str):
    return patch(RK, Mock(side_effect=keys))
