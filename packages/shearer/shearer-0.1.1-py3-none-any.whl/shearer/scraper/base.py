
from abc import ABC, abstractmethod
from typing import Any, Union

from ..models import PageSchema, ScrappingOptions


class Scraper(ABC):

    def __init__(self, options: ScrappingOptions, **kwargs: Any):
        self.options: Union[options, None] = options
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def get_page_schema(self) -> PageSchema:
        """Method to define content schema"""
        pass

    @abstractmethod
    def scrape(self):
        """Scrape the content from the given URL"""
        pass
