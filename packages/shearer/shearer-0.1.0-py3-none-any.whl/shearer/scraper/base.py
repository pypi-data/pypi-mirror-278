
from abc import ABC, abstractmethod
from typing import Any
from ..models import SiteSchema, ScrappedResults, ScrappingOptions


class Scraper(ABC):

    def __init__(self, options: ScrappingOptions, **kwargs: Any):
        self.options = options
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def get_site_schema(self):
        """Method to define content schema"""
        pass

    @abstractmethod
    def scrape(self):
        """Scrape the content from the given URL"""
        pass
