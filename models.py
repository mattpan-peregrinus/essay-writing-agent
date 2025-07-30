"""Model configurations for the essay writer."""

import os
from typing import List
try:
    from pydantic import BaseModel
except ImportError:
    from pydantic.v1 import BaseModel

from langchain_openai import ChatOpenAI
from tavily import TavilyClient


class Queries(BaseModel):
    queries: List[str]


def get_model():
    """Get OpenAI model."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def get_search():
    """Get Tavily search client."""
    if not os.environ.get("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY environment variable is required")
    
    return TavilyClient(api_key=os.environ["TAVILY_API_KEY"])