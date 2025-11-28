"""
Gemini LLM Client - Updated for google-genai SDK (New v1.0+)
Supports Gemini 1.5 Flash / Pro
"""

from google import genai
from google.genai import types
from typing import List, Dict, Any, Optional
import logging
import json
import re

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Wrapper for Google Gemini API using the new google-genai SDK.
    Provides text, JSON, and chat generation.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash",
        temperature: float = 0.7,
        max_output_tokens: int = 2048
    ):
        """
        Initialize the Gemini client.

        Args:
            api_key: Google Gemini API key
            model: Model name (e.g., gemini-2.0-flash, gemini-1.5-flash)
            temperature: Creativity level (0–1)
            max_output_tokens: Token limit for responses
        """
        self.api_key = api_key
        self.model_name = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

        try:
            self.client = genai.Client(api_key=api_key)
            logger.info(f"✅ Initialized GeminiClient (google-genai) with model '{model}'")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")
            raise

    # ----------------------------------------------------------------------
    def generate(self, prompt: str) -> str:
        """
        Generate plain text output.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens
                )
            )
            if not response.text:
                raise ValueError("Gemini returned an empty response.")
            return response.text
        except Exception as e:
            logger.error(f"❌ Error generating text: {e}")
            raise

    # ----------------------------------------------------------------------
    def generate_json(
        self,
        prompt: str,
        response_schema: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate structured JSON from a prompt.
        Uses response_mime_type='application/json' for better reliability.
        """
        try:
            system_prompt = (
                "Respond ONLY in JSON format. "
                "Do not include markdown, explanations, or any text outside valid JSON."
            )

            full_prompt = f"{system_prompt}\n\n{prompt}"

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens,
                    response_mime_type="application/json"
                )
            )
            text = response.text

            if not text:
                raise ValueError("Gemini returned an empty response.")

            logger.info(f"[Gemini raw preview] {text[:300]}...")
            
            # Even with JSON mode, sometimes we might want to clean it
            # But usually it returns pure JSON.
            return text

        except Exception as e:
            logger.error(f"❌ Error generating JSON: {e}")
            return "{}"

    # ----------------------------------------------------------------------
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Multi-turn conversation.
        """
        try:
            # Convert messages to Gemini format
            # The new SDK uses a slightly different history format if using chats.create
            # But we can also just pass the full history to generate_content if we manage it manually.
            # Or use the chat feature.
            
            history = []
            last_message = ""
            
            # Separate history and last message
            if messages:
                last_message = messages[-1]['content']
                
                for m in messages[:-1]:
                    role = "user" if m['role'] == 'user' else "model"
                    history.append(types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=m['content'])]
                    ))

            chat = self.client.chats.create(
                model=self.model_name,
                history=history,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens
                )
            )
            
            response = chat.send_message(last_message)
            return response.text
        except Exception as e:
            logger.error(f"❌ Chat generation failed: {e}")
            raise

    # ----------------------------------------------------------------------
    def generate_with_context(
        self,
        question: str,
        context: str,
        system_instruction: str
    ) -> str:
        """
        RAG-style generation with provided context.
        """
        prompt = f"""
System Instruction:
{system_instruction}

Context:
{context}

Question: {question}
"""
        return self.generate(prompt)

    # ----------------------------------------------------------------------
    def count_tokens(self, text: str) -> int:
        """
        Estimate tokens.
        """
        try:
            # The new SDK might have a different way, but often we can just use the model
            # or a rough estimate if the method isn't directly exposed on the client easily.
            # For now, let's try the count_tokens method if available on the model endpoint.
            response = self.client.models.count_tokens(
                model=self.model_name,
                contents=text
            )
            return response.total_tokens
        except Exception:
            return len(text.split())  # rough estimate
