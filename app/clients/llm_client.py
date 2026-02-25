import os
import logging
from typing import Optional

from openai import OpenAI
from openai import AuthenticationError, RateLimitError, APIConnectionError, OpenAIError
import app.config as config

logger = logging.getLogger(__name__)

OPENAI_API_KEY = config.Config.OPENAI_API_KEY
OPENAI_MODEL = config.Config.OPENAI_MODEL
OPENAI_MAX_TOKENS = config.Config.OPENAI_MAX_TOKENS
OPENAI_TEMPERATURE = config.Config.OPENAI_TEMPERATURE

class LLMClient:
    """
    Low-level OpenAI API client.
    Responsible ONLY for connecting to OpenAI and sending chat requests.
    Summarization logic lives in services/summarizer/ai_summarizer.py
    """

    def __init__(
        self,
        api_key: Optional[str] = OPENAI_API_KEY,
        model: str = OPENAI_MODEL,
        max_tokens: int = OPENAI_MAX_TOKENS,
        temperature: float = OPENAI_TEMPERATURE,
    ):
        """
        Initialize the OpenAI client.

        Args:
            api_key (str): OpenAI API key. Defaults to OPENAI_API_KEY env variable.
            model (str): GPT model to use.
            max_tokens (int): Max tokens for the response.
            temperature (float): Sampling temperature.
        """
        self.api_key = api_key

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Set OPENAI_API_KEY in your .env file or pass it directly."
            )

        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = OpenAI(api_key=self.api_key)

        logger.info(f"LLMClient initialized with model: {self.model}")

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a chat request to OpenAI and return the response text.

        Args:
            system_prompt (str): Instructions for the AI role/behavior.
            user_prompt (str): The actual user message / content to process.

        Returns:
            str: The model's response text.
        """
        try:
            logger.info(f"Sending request to OpenAI model: {self.model}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            result = response.choices[0].message.content.strip()
            logger.info("OpenAI response received successfully.")
            return result

        except AuthenticationError:
            logger.error("Invalid OpenAI API key.")
            raise ValueError("Invalid OpenAI API key. Please check your OPENAI_API_KEY.")

        except RateLimitError:
            logger.error("OpenAI rate limit exceeded.")
            raise RuntimeError("OpenAI rate limit exceeded. Please wait and try again.")

        except APIConnectionError:
            logger.error("Failed to connect to OpenAI API.")
            raise RuntimeError("Could not connect to OpenAI API. Check your internet connection.")

        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise RuntimeError(f"OpenAI API error: {e}") from e