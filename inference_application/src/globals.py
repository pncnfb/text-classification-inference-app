from configparser import ConfigParser

from src.controller import MistralClient, DomainPredictor
from src.agents import NotesAgent

config = ConfigParser()
config.read("config.ini")

ocr_client = MistralClient(api_key=config["MISTRAL_AI"]["API_KEY"])
domain_predictor = DomainPredictor(model_path=config["DOMAIN_PREDICTOR"]["MODEL_PATH"],
                                   vectorizer_path=config["DOMAIN_PREDICTOR"]["VECTORIZER_PATH"])
notes_agent = NotesAgent(config["NOTES_AGENT"])