import time
import os
import json
from utils.logger import setup_logger
from kafka.connection import connect_kafka
from config import EVENTS_PER_BATCH, BATCH_INTERVAL
from events.processFileAfterImport import process_file_after_import

logger = setup_logger()

def run_producer(file_content: bytes, filename: str):
    kafka = connect_kafka()
    success = False
    kafkaTopic = os.getenv("KAFKA_TOPIC")

    if not kafka:
        logger.error("Falha ao conectar ao Kafka")
        process_file_after_import(filename, success)
        return

    events_topic = kafka.topic(name=kafkaTopic, value_serializer="json")

    try:
        events = json.loads(file_content)
    except Exception as e:
        logger.error(f"Erro ao carregar eventos do conteúdo do arquivo: {e}")
        process_file_after_import(filename, success)
        return

    if not events:
        logger.error(f"Nenhum evento carregado do conteúdo do arquivo {filename}")
        process_file_after_import(filename, success)
        return

    with kafka.get_producer() as producer:
        try:
            for i in range(0, len(events), EVENTS_PER_BATCH):
                batch = events[i:i + EVENTS_PER_BATCH]

                for event in batch:
                    logger.info(f"Evento do arquivo: {event}")

                    kafka_msg = events_topic.serialize(key=event["event_type"], value=event)

                    producer.produce(
                        topic=events_topic.name,
                        key=kafka_msg.key,
                        value=kafka_msg.value,
                    )

                    logger.info(f"Evento enviado: {event}")

                logger.info(f"Lote de {len(batch)} eventos publicados. Aguardando {BATCH_INTERVAL} segundos...")
                time.sleep(BATCH_INTERVAL)

            success = True
            logger.info(f"Importação do conteúdo do arquivo {filename} concluída com sucesso")

        except KeyboardInterrupt:
            logger.info("Produtor encerrado pelo usuário")
        except Exception as e:
            logger.error(f"Erro: {e}")
        finally:
            process_file_after_import(filename, success)
