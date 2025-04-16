import logging
from kafka.producer import run_producer

def main():
    run_producer()


if __name__ == "__main__":
    try:
        logging.basicConfig(level="DEBUG")
        main()
    except KeyboardInterrupt:
        pass
