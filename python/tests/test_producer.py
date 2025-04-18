# tests/test_producer.py
from unittest.mock import MagicMock, patch
from service.producer import run_producer

@patch("service.producer.connect_kafka")
@patch("service.producer.load_events_from_file")
def test_run_producer_success(mock_load_events, mock_connect_kafka):
    mock_events = [{"event_type": "login", "user": "john"}]
    mock_load_events.return_value = mock_events

    mock_kafka = MagicMock()
    mock_topic = MagicMock()
    mock_producer_ctx = MagicMock()
    mock_producer = MagicMock()

    mock_kafka.topic.return_value = mock_topic
    mock_kafka.get_producer.return_value = mock_producer_ctx
    mock_producer_ctx.__enter__.return_value = mock_producer
    mock_connect_kafka.return_value = mock_kafka

    with patch("service.producer.logger") as mock_logger:
        run_producer("some_file.json")
        mock_logger.info.assert_any_call(f"Evento enviado: {mock_events[0]}")

@patch("service.producer.connect_kafka")
@patch("service.producer.load_events_from_file")
def test_run_producer_empty_events(mock_load_events, mock_connect_kafka):
    mock_load_events.return_value = []

    mock_kafka = MagicMock()
    mock_connect_kafka.return_value = mock_kafka

    with patch("service.producer.logger"):
        run_producer("empty_file.json")

@patch("service.producer.connect_kafka")
@patch("service.producer.load_events_from_file")
def test_run_producer_exception_handling(mock_load_events, mock_connect_kafka):
    mock_events = [{"event_type": "login", "user": "john"}]
    mock_load_events.return_value = mock_events

    mock_kafka = MagicMock()
    mock_producer_ctx = MagicMock()
    mock_producer = MagicMock()
    mock_producer.produce.side_effect = Exception("Test exception")

    mock_producer_ctx.__enter__.return_value = mock_producer
    mock_kafka.get_producer.return_value = mock_producer_ctx
    mock_connect_kafka.return_value = mock_kafka
    mock_kafka.topic.return_value.serialize.return_value = MagicMock(key="k", value="v")

    with patch("service.producer.logger") as mock_logger:
        run_producer("some_file.json")
        mock_logger.error.assert_called_with("Erro: Test exception")

@patch("service.producer.connect_kafka")
@patch("service.producer.load_events_from_file")
def test_run_producer_keyboard_interrupt(mock_load_events, mock_connect_kafka):
    mock_events = [{"event_type": "login", "user": "john"}]
    mock_load_events.return_value = mock_events

    mock_kafka = MagicMock()
    mock_producer_ctx = MagicMock()
    mock_producer = MagicMock()

    mock_producer_ctx.__enter__.return_value = mock_producer
    mock_kafka.get_producer.return_value = mock_producer_ctx
    mock_connect_kafka.return_value = mock_kafka
    mock_kafka.topic.return_value.serialize.return_value = MagicMock(key="k", value="v")

    with patch("service.producer.logger") as mock_logger, \
         patch("time.sleep", side_effect=KeyboardInterrupt):
        run_producer("some_file.json")
        mock_logger.info.assert_called_with("Produtor encerrado pelo usuário")
