import requests
import json
import pandas as pd

from openai import OpenAI
from bs4 import BeautifulSoup
from typing import List, Union

from .base import Scraper
from ..prompts.xml import PROMPT_PREFIX, USER_INSTRUCTION
from ..models import PageSchema, ScrappingOptions
from ..utils import get_token_num
from ..configs.llm import MAX_INPUT_TOKEN

def get_entries_by_key(soup: BeautifulSoup, path, key: str):
        # Find key in path
        for item in path:
            if item == key:
                return soup.find_all(item)
            else:
                continue

def get_text_for_paths(soup: BeautifulSoup, paths: List[str], key: str):
    results = dict(records=[])
    result = {path[-1] : [] for path in paths}

    for path in paths:
        entries = get_entries_by_key(soup, path, key)
        for entry in entries:
            path_result = [item.text 
                           if item.text!='' 
                           else str(item) 
                           for item in entry.find_all(path[-1])]
            result[path[-1]].append(path_result)

    results["records"] = pd.DataFrame(result).to_dict(orient="records")
    return results

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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
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
    page_schema: PageSchema = None

    @classmethod
    def from_input_options(cls, client: OpenAI, options: ScrappingOptions, **kwargs) -> Scraper:
        return cls(client=client, options=options, **kwargs)
    

    def get_page_schema(self, url: str) -> PageSchema:
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
        if self.options is not None:
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
            page_schema_response = response.choices[0].message.content
            page_schema = PageSchema(page_schema=json.loads(page_schema_response))
            self.page_schema = page_schema
            return page_schema

        else:
            raise TypeError(f"""Missing ScrappingOptions object, options variable in XMLScraper
                                is provided as type of {type(self.options)} instead.

                                To resolve this error, please provide the options variable
                                as an instance of ScrappingOptions.

                                Example:
                                ```
                                options = ScrappingOptions(model="gpt-4o", 
                                                           temperature=0.0, 
                                                           content_type="xml", 
                                                           required_data="author name, article title, article_url")
                                scraper = XMLScraper.from_input_options(client=client, options=options)
                                ```python\n
                             
                               """)
    
    def scrape_url(self, url: str, key: str):
        if self.page_schema is None:
            self.get_page_schema(url)

        page_content = fetch_content(url)
        paths = list(trace_keys(self.page_schema.page_schema, 'target_field'))
        return get_text_for_paths(page_content, paths, key)
       
    def scrape(self, url: Union[str, List[str]], key: str, page_schema: PageSchema = None):
        if page_schema is not None:
            self.page_schema = page_schema
        if isinstance(url, str):
            results = self.scrape_url(url, key)
        else:
            results = []
            for target in url:
                result = self.scrape_url(target, key)
                results.append(result)

        return results

    
