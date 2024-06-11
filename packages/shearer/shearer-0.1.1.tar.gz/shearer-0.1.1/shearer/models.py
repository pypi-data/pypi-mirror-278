from enum import Enum

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, Union

OPENAI_TOKEN_LIMITS = {
    "models" : {
        "gpt-4-turbo": 4096
    }
}


class PageSchema(BaseModel):
    page_schema: Union[str, Dict[str, Any]]

class ScrappedResults(BaseModel):
    url: str
    content: str
    source_type: Literal["html", "xml", "json"]
    site_schema: PageSchema = None

    class Config:
        allow_extra = True

class ScrappingOptions(BaseModel):
    model: Literal["gpt-4-turbo", "gpt-4o"] = "gpt-4o"
    temperature: float = 0.0
    content_type: Literal["xml", "html", "json"]
    required_data: str
