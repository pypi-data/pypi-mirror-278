from abc import ABC, abstractmethod
from typing import Any


class BaseLogistic(ABC):
    # @abstractmethod
    # def publish(self, topic, payload):
    #     """
    #     Abstract method that packages the payload.
    #     """
    #     pass


    def subscribe(self, topic):
        """
        Abstract method that packages the payload.
        """
        pass


    # @abstractmethod
    # def pack(self, payload) -> (str, Any):
    #     """
    #     Abstract method that packages the payload.
    #     """
    #     pass


    # @abstractmethod
    # def unpack(self, payload):
    #     """
    #     Abstract method that unpacks the payload.
    #     """
    #     pass
    