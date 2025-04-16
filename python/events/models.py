import random

def create_event_payload(event_type):
    if event_type == 'click':
        return {
            'button_id': str(random.randint(1, 10))
        }
    elif event_type == 'login':
        return {
            'device': random.choice(['mobile', 'desktop', 'tablet'])
        }
    elif event_type == 'purchase':
        return {
            'item_id': str(random.randint(1, 50)), 
            'price': str(round(random.uniform(0.99, 99.99), 2))
        }
    elif event_type == 'game_start':
        return {
            'level': str(random.randint(1, 10))
        }
    elif event_type == 'game_end':
        return {
            'score': str(random.randint(0, 1000)), 
            'duration': str(random.randint(30, 3600))
        }
    else:
        return {}