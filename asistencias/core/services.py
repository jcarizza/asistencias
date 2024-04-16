import requests
from django.conf import settings

import logging


logger = logging.getLogger(__name__)


class CircuitBreak:
    __instance = None
    __timeout = settings.CIRCUIT_TIMEOUT
    __is_open = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(CircuitBreak, cls).__new__(cls)
        return cls.__instance

    def dummy_call(self):
        return {
            "clima": "it's raining man"
        }

    def close_circuit(self):
        self.__is_open = False

    def call(self, url):
        logger.info(f"CircuitBreak Status={self.__is_open}")
        if self.__is_open:
            logger.info("CircuitBreak is open returning dummy call")
            return self.dummy_call()

        try:
            logger.info("Calling Weather API")
            response = requests.get(url, timeout=self.__timeout)
            logger.info("Weather API success")
            response.raise_for_status()
            return response.json()
        except (ConnectionError, TimeoutError, requests.exceptions.HTTPError) as exc:
            logger.error("Weather API has failed, activating CircuitBreak")
            self.__is_open = True
            return self.dummy_call()
        except Exception as exc:
            logger.error("General error Weather API has failed, activating CircuitBreak")
            self.__is_open = True
            return self.dummy_call()


class ClimaService(CircuitBreak):

    @staticmethod
    def get_clima():
        circuit_break = CircuitBreak()
        response = circuit_break.call(settings.WEATHER_API_URL)
        return response["clima"]
