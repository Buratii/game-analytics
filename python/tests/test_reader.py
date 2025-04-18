import json
from unittest.mock import mock_open, patch
from events.reader import load_events_from_file

def test_load_events_from_file_success():
    mock_data = json.dumps([
        {"event_type": "login", "user": "john"},
        {"event_type": "logout", "user": "alice"}
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("events.reader.logger") as mock_logger:
            result = load_events_from_file("dummy_path.json")
            assert len(result) == 2
            assert result[0]["event_type"] == "login"
            mock_logger.info.assert_called()

def test_load_events_from_file_failure():
    with patch("builtins.open", side_effect=Exception("file error")):
        with patch("events.reader.logger") as mock_logger:
            result = load_events_from_file("bad_path.json")
            assert result == []
            mock_logger.error.assert_called()
