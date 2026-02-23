"""LangStruct-based information extractor for CIDOC CRM entity extraction."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from infoextract_cidoc.extraction.lite_schema import LiteExtractionResult

_DEFAULT_MODEL = "gemini/gemini-2.5-flash"

SYSTEM_PROMPT = """You are a CIDOC CRM expert extracting structured information from text.

Extract entities and relationships following the CIDOC Conceptual Reference Model v7.1.3.

Entity types:
- Person (E21): individuals - use ref_id like "person_1", "person_2"
- Event (E5): historical or biographical events - use ref_id like "event_1"
- Place (E53): geographic locations - use ref_id like "place_1"
- Object (E22): human-made objects, artifacts - use ref_id like "object_1"
- TimeSpan (E52): time spans or dates - use ref_id like "timespan_1"

Common property codes:
- P98: was born (Person -> Place/Event)
- P100: died in (Person -> Event)
- P7: took place at (Event -> Place)
- P4: has time-span (Event -> TimeSpan)
- P11: had participant (Event -> Person)
- P14: carried out by (Event -> Person)
- P108: has produced (Event/Person -> Object)
- P1: is identified by (any -> any)

Confidence scoring:
- 0.9-1.0: directly stated facts
- 0.7-0.8: clearly implied
- 0.5-0.6: inferred
- 0.3-0.4: uncertain inference

Use consistent ref_ids (e.g. "person_1") and reference them exactly in relationships.
"""


class LangStructExtractor:
    """LangStruct-based extractor for CIDOC CRM entities.

    Wraps LangStruct with the LiteExtractionResult schema for single-pass
    entity and relationship extraction from unstructured text.

    Args:
        model: LiteLLM-compatible model string. Defaults to LANGSTRUCT_DEFAULT_MODEL
               environment variable, or "gemini/gemini-2.5-flash" if not set.
    """

    def __init__(self, model: str | None = None) -> None:
        self._model = model or os.environ.get(
            "LANGSTRUCT_DEFAULT_MODEL", _DEFAULT_MODEL
        )
        self._extractor: Any = None

    def _get_extractor(self) -> Any:
        """Lazily initialize the LangStruct extractor."""
        if self._extractor is None:
            try:
                from langstruct import LangStruct  # type: ignore[import]
            except ImportError as e:
                msg = (
                    "langstruct is required for LangStructExtractor. "
                    "Install it with: pip install langstruct"
                )
                raise ImportError(msg) from e

            self._extractor = LangStruct(
                schema=LiteExtractionResult,
                model=self._model,
                system_prompt=SYSTEM_PROMPT,
            )
        return self._extractor

    def extract(self, text: str) -> LiteExtractionResult:
        """Extract entities and relationships from text (synchronous).

        Args:
            text: The input text to extract from.

        Returns:
            LiteExtractionResult with entities and relationships.
        """
        extractor = self._get_extractor()
        return extractor(text)

    async def extract_async(self, text: str) -> LiteExtractionResult:
        """Extract entities and relationships from text (asynchronous).

        Wraps the synchronous extract() in asyncio.to_thread.

        Args:
            text: The input text to extract from.

        Returns:
            LiteExtractionResult with entities and relationships.
        """
        return await asyncio.to_thread(self.extract, text)

    def extract_batch(self, texts: list[str]) -> list[LiteExtractionResult]:
        """Extract from multiple texts.

        Args:
            texts: List of input texts.

        Returns:
            List of LiteExtractionResult, one per input text.
        """
        return [self.extract(text) for text in texts]

    def optimize(self, texts: list[str], expected: list[LiteExtractionResult]) -> None:
        """Run DSPy optimization on the extractor.

        Args:
            texts: Training input texts.
            expected: Expected LiteExtractionResult outputs.
        """
        extractor = self._get_extractor()
        if hasattr(extractor, "optimize"):
            extractor.optimize(texts, expected)

    def save(self, path: str | Path) -> None:
        """Save the extractor state to disk.

        Args:
            path: File path to save to.
        """
        extractor = self._get_extractor()
        if hasattr(extractor, "save"):
            extractor.save(str(path))

    def load(self, path: str | Path) -> None:
        """Load extractor state from disk.

        Args:
            path: File path to load from.
        """
        extractor = self._get_extractor()
        if hasattr(extractor, "load"):
            extractor.load(str(path))

    @property
    def model(self) -> str:
        """The model being used for extraction."""
        return self._model
