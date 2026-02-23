"""Unit tests for LangStructExtractor (mocked LangStruct)."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from infoextract_cidoc.extraction.langstruct_extractor import LangStructExtractor
from infoextract_cidoc.extraction.lite_schema import LiteEntity, LiteExtractionResult


@pytest.fixture
def mock_lite_result() -> LiteExtractionResult:
    return LiteExtractionResult(
        entities=[
            LiteEntity(ref_id="person_1", entity_type="Person", label="Einstein"),
        ],
        relationships=[],
    )


@pytest.mark.unit
class TestLangStructExtractor:
    def test_default_model(self) -> None:
        extractor = LangStructExtractor()
        assert extractor.model == "gemini/gemini-3-flash-preview"

    def test_custom_model(self) -> None:
        extractor = LangStructExtractor(model="openai/gpt-4o-mini")
        assert extractor.model == "openai/gpt-4o-mini"

    def test_model_from_env(self, monkeypatch) -> None:
        monkeypatch.setenv("LANGSTRUCT_DEFAULT_MODEL", "anthropic/claude-3-haiku")
        extractor = LangStructExtractor()
        assert extractor.model == "anthropic/claude-3-haiku"

    def test_extract_calls_langstruct(self, mock_lite_result) -> None:
        mock_extract_result = MagicMock()
        mock_extract_result.entities = mock_lite_result.model_dump()
        mock_ls_instance = MagicMock()
        mock_ls_instance.extract.return_value = mock_extract_result
        mock_ls_class = MagicMock(return_value=mock_ls_instance)

        with patch.dict(
            "sys.modules", {"langstruct": MagicMock(LangStruct=mock_ls_class)}
        ):
            extractor = LangStructExtractor()
            result = extractor.extract("Einstein was born in Ulm.")

        assert result == mock_lite_result
        mock_ls_instance.extract.assert_called_once_with("Einstein was born in Ulm.")

    def test_extract_batch(self, mock_lite_result) -> None:
        mock_extract_result = MagicMock()
        mock_extract_result.entities = mock_lite_result.model_dump()
        mock_ls_instance = MagicMock()
        mock_ls_instance.extract.return_value = mock_extract_result
        mock_ls_class = MagicMock(return_value=mock_ls_instance)

        with patch.dict(
            "sys.modules", {"langstruct": MagicMock(LangStruct=mock_ls_class)}
        ):
            extractor = LangStructExtractor()
            results = extractor.extract_batch(["text 1", "text 2"])

        assert len(results) == 2
        assert all(r == mock_lite_result for r in results)

    def test_missing_langstruct_raises(self) -> None:
        with patch.dict("sys.modules", {"langstruct": None}):
            extractor = LangStructExtractor()
            extractor._extractor = None  # force lazy init
            with pytest.raises(ImportError, match="langstruct is required"):
                extractor.extract("text")

    def test_extract_async(self, mock_lite_result) -> None:
        mock_extract_result = MagicMock()
        mock_extract_result.entities = mock_lite_result.model_dump()
        mock_ls_instance = MagicMock()
        mock_ls_instance.extract.return_value = mock_extract_result
        mock_ls_class = MagicMock(return_value=mock_ls_instance)

        with patch.dict(
            "sys.modules", {"langstruct": MagicMock(LangStruct=mock_ls_class)}
        ):
            extractor = LangStructExtractor()
            result = asyncio.run(extractor.extract_async("Einstein was born in Ulm."))

        assert result == mock_lite_result
