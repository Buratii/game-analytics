KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'user-events'
KAFKA_MAX_RETRIES = 10
KAFKA_RETRY_INTERVAL = 5  # segundos

# Configuração de eventos
EVENT_TYPES = ['click', 'login', 'purchase', 'game_start', 'game_end']
GAME_IDS = ['123', '456', '789', '101', '202']
NUM_USERS = 100
EVENTS_PER_BATCH = 10
BATCH_INTERVAL = 5  # segundos