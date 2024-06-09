import requests
import json

from collections import defaultdict

from openai import OpenAI
from bs4 import BeautifulSoup
from typing import List, Union


from .base import Scraper
from ..prompts import PROMPT_PREFIX, USER_INSTRUCTION
from ..models import SiteSchema, ScrappedResults, ScrappingOptions
from ..utils import get_token_num
from ..configs.llm import MAX_INPUT_TOKEN

def get_text_for_paths(soup, paths):
    result = defaultdict(list)
    
    for path in paths:
        elements = [soup]
        for tag in path:
            temp_elements = []
            for element in elements:
                temp_elements.extend(element.find_all(tag))
            elements = temp_elements
        
        # Get text from the last tag in the path
        last_tag = path[-1]
        for element in elements:
            result[last_tag].append(element.get_text())
    
    return dict(result)

def trace_keys(d, target_value="target_field", current_path=None):
    if current_path is None:
        current_path = []

    # Iterate through the dictionary
    for key, value in d.items():
        new_path = current_path + [key]
        
        # If the value is a dictionary, recurse
        if isinstance(value, dict):
            yield from trace_keys(value, target_value, new_path)
        # If the value matches the target value, yield the path
        elif value == target_value:
            yield new_path

def fetch_content(url: str) -> BeautifulSoup:
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    # Fetch the content from the URL with headers
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')
        return soup

    else:
        raise Exception(f"Failed to fetch the content from {url},\
                         received status code: {response.status_code}")

class XMLScraper(Scraper):
    client: OpenAI
    site_schema: SiteSchema = None
    @classmethod
    def from_input_options(cls, client: OpenAI, options: ScrappingOptions) -> Scraper:
        return cls(client=client, options=options)

    def get_site_schema(self, url: str) -> SiteSchema:
        soup = fetch_content(url)
        page_content = soup.prettify()
        total_tokens = get_token_num(page_content)

        if total_tokens > MAX_INPUT_TOKEN:
            batch_token_size = 0
            max_token = total_tokens
            while batch_token_size > MAX_INPUT_TOKEN:
                max_token = max_token / 2
                page_content = page_content[:max_token]
                batch_token_size = get_token_num(page_content)

            page_content = page_content[:max_token]

        response = self.client.chat.completions.create(
            model=self.options.model,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system",
                "content": "You are a helpful assistant designed to output JSON."},
                {"role": "system", 
                "content": PROMPT_PREFIX.format(CONTENT_TYPE=self.options.content_type,
                                                                REQUIRED_DATA=self.options.required_data)},
                {"role": "user", 
                "content": USER_INSTRUCTION.format(XML_OBJECT=page_content)},
                ]
        )
        site_schema_response = response.choices[0].message.content
        site_schema = SiteSchema(site_schema=json.loads(site_schema_response))
        self.site_schema = site_schema
        return site_schema
    
    def scrape_url(self, url: str):
        if self.site_schema is None:
            self.get_site_schema(url)

        page_content = fetch_content(url)
        
        paths = list(trace_keys(self.site_schema.site_schema, 'target_field'))

        texts = get_text_for_paths(page_content, paths)

        return texts
       
    def scrape(self, url: Union[str, List[str]]):
        if isinstance(url, str):
            results = self.scrape_url(url)
        else:
            results = []
            for target in url:
                result = self.scrape_url(target)
                results.append(result)

        return results

    
