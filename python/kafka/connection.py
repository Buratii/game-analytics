import time
import os
from quixstreams import Application
from utils.logger import setup_logger
from config import KAFKA_MAX_RETRIES, KAFKA_RETRY_INTERVAL

logger = setup_logger()

def connect_kafka():
  retries = 0

  kafkaBroker = os.getenv("KAFKA_BROKER")

  while retries < KAFKA_MAX_RETRIES:
    try:
      app = Application(
          broker_address=kafkaBroker,
          loglevel="DEBUG",
          consumer_group="analytics_reader",
          auto_offset_reset="earliest",
      )

      return app
    except Exception as e:
      logger.warning(f"Falha ao conectar ao Kafka (tentativa {retries+1}/{KAFKA_MAX_RETRIES}): {e}")
      retries += 1
      time.sleep(KAFKA_RETRY_INTERVAL)
    
  logger.error(f"Falha ao conectar ao Kafka após {KAFKA_MAX_RETRIES} tentativas")
  return None
  
