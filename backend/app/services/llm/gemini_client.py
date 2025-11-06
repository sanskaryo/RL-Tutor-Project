"""
Gemini LLM Client - Updated for 2025 SDK (google-genai)
Supports Gemini 2.5 Flash / Pro / Flash-Lite
"""

from google import genai
from typing import List, Dict, Any, Optional
import logging
import json
import re

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Wrapper for Google Gemini API using new unified SDK.
    Provides text, JSON, and chat generation.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_output_tokens: int = 2048
    ):
        """
        Initialize the Gemini client.

        Args:
            api_key: Google Gemini API key
            model: Model name (e.g., gemini-2.5-flash, gemini-2.5-pro)
            temperature: Creativity level (0–1)
            max_output_tokens: Token limit for responses
        """
        self.api_key = api_key
        self.model_name = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

        try:
            self.client = genai.Client(api_key=api_key)
            logger.info(f"✅ Initialized GeminiClient with model '{model}'")
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
                contents=prompt
            )
            text = getattr(response, "text", None)
            if not text:
                raise ValueError("Gemini returned an empty response.")
            return text
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
        Ensures valid JSON format even if the LLM returns mixed text.
        """
        try:
            system_prompt = (
                "Respond ONLY in JSON format. "
                "Do not include markdown, explanations, or any text outside valid JSON."
            )

            full_prompt = f"{system_prompt}\n\n{prompt}"

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt
            )

            text = getattr(response, "text", None)
            if not text:
                raise ValueError("Gemini returned an empty response.")

            logger.info(f"[Gemini raw preview] {text[:300]}...")

            # Try to extract valid JSON block
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                json_str = match.group(0)
                json.loads(json_str)  # validate
                return json_str
            else:
                logger.warning("⚠ No valid JSON detected. Returning raw text.")
                return text.strip()

        except Exception as e:
            logger.error(f"❌ Error generating JSON: {e}")
            return "{}"

    # ----------------------------------------------------------------------
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Multi-turn conversation.
        """
        try:
            conversation = "\n".join(
                [f"{m['role']}: {m['content']}" for m in messages]
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=conversation
            )
            return getattr(response, "text", "")
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

Answer based ONLY on the context above.
"""
        return self.generate(prompt)

    # ----------------------------------------------------------------------
    def count_tokens(self, text: str) -> int:
        """
        Estimate tokens (Gemini 2.5 SDK doesn’t expose token counter yet).
        """
        try:
            return len(text.split())  # rough estimate
        except Exception:
            return len(text) // 4
