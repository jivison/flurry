from dataclasses import dataclass
import json


@dataclass
class Config:
    discord_token: str
    zephyr_id: int
    flurry_id: int


def get_config() -> Config:
    with open("bot.json", "r") as config_file:
        raw_config = json.load(config_file)
        return Config(discord_token=raw_config['discord_token'], zephyr_id=raw_config['zephyr_id'], flurry_id=raw_config['flurry_id'])
