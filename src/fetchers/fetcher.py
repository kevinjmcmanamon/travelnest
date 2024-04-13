from abc import ABC, abstractmethod


class Fetcher(ABC):

    @abstractmethod
    def get_data(self, path):
        pass