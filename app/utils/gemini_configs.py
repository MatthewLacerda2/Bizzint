import logging
import numpy as np
from typing import Any
from dotenv import load_dotenv
from google.genai import Client
from google.genai.types import GenerateContentConfig, EmbedContentConfig
from ..core.config import Settings
from .envs import NUM_DIMENSIONS

logger = logging.getLogger(__name__)
load_dotenv()

def get_client():
    return Client(api_key=Settings.GEMINI_API_KEY)

def get_gemini_json_config(json_schema: dict[str, Any]) -> GenerateContentConfig:
    return GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=json_schema,
    )

def get_gemini_text_config() -> GenerateContentConfig:
    return GenerateContentConfig(
        response_mime_type='text/plain',
    )

def get_gemini_embedding_config(text: str) -> np.ndarray:
    
    client = get_client()
    
    response = client.models.embed_content(
        model="gemini-embedding-002",
        contents=text,
        config=EmbedContentConfig(
            output_dimensionality=NUM_DIMENSIONS,
        ),
    )
    
    embedding_values = response.embeddings[0].values
    return np.array(embedding_values, dtype=np.float32)