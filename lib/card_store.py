from typing import Dict, Optional
from dataclasses import dataclass
from PIL import Image


@dataclass
class Card:
    card: Image.Image
    description: str


class CardStore:
    store: Dict[int, Image.Image] = {}

    def __init__(self):
        pass

    def add_card(self, user_id: int, image: Image.Image, description: str) -> Card:
        card = Card(card=image, description=description)

        self.store[user_id] = card

        return card

    def get_card(self, user_id) -> Optional[Card]:
        if user_id in self.store:
            return self.store[user_id]
        else:
            return None
