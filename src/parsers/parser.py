from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


NOT_FOUND = "Attribute cannot be found within HTML content"


class Parser(ABC):
    @abstractmethod
    def get_property_attributes(self, html):
        pass
