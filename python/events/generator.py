"""
Gerador de eventos de usuário para jogos
"""
import random
from datetime import datetime
from faker import Faker
from config import EVENT_TYPES, GAME_IDS, NUM_USERS
from events.models import create_event_payload
from utils.logger import setup_logger

logger = setup_logger()
fake = Faker()

# Melhoria: Criar um gerador de evento abstrato para diferentes tipos de eventos

class EventGenerator:
    def __init__(self):
        self.fake = Faker()
    
    def generate_event(self):
        user_id = str(random.randint(1, NUM_USERS))
        event_type = random.choice(EVENT_TYPES)
        timestamp = datetime.now().isoformat()
        game_id = random.choice(GAME_IDS)
        
        payload = create_event_payload(event_type)
        
        event = {
            "user_id": user_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "game_id": game_id,
            "payload": payload
        }
        
        return event