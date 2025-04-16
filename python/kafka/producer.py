import json
import time
from utils.logger import setup_logger
from kafka.connection import connect_kafka
from config import EVENTS_PER_BATCH, BATCH_INTERVAL
from events.generator import EventGenerator

logger = setup_logger()

def run_producer():
  kafka = connect_kafka();

  if not connect_kafka():
    logger.error("Falha ao conectar ao Kafka")
    return

  if kafka is None:
    logger.error("Kafka não está disponível")
    return
  
  generator = EventGenerator()

  events_topic = kafka.topic(name="events", value_serializer="json")

  with kafka.get_producer() as producer:
    try:
      while True:
        for _ in range(EVENTS_PER_BATCH):
          event = generator.generate_event()

          logger.info(f"Evento gerado: {event}")
        
          kafka_msg = events_topic.serialize(key=event["event_type"], value=event)

          producer.produce(
            topic=events_topic.name,
            key=kafka_msg.key,
            value=kafka_msg.value,
          )
          
          logger.info(f"Lote de {EVENTS_PER_BATCH} eventos publicados. Aguardando {BATCH_INTERVAL} segundos...")
          logger.info(f"Evento enviado: {event}")
          time.sleep(BATCH_INTERVAL)
    except KeyboardInterrupt:
      logger.info("Produtor encerrado pelo usuário")
    except Exception as e:
      logger.error(f"Erro: {e}")