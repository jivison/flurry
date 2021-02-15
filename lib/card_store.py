from typing import Dict, Optional
from PIL import Image


class CardStore:
    store: Dict[int, Image.Image] = {}

    def __init__(self):
        pass

    def add_card(self, user_id: int, card: Image.Image) -> None:
        self.store[user_id] = card

    def get_card(self, user_id) -> Optional[Image.Image]:
        if user_id in self.store:
            return self.store[user_id]
        else:
            return None
