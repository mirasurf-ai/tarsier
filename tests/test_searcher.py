"""
Tests for TarsierSearcher class.
"""

import unittest
from unittest.mock import MagicMock, patch

import pytest
from meilisearch import Client as MeiliClient
from qdrant_client import QdrantClient

from tarsier.searcher import TarsierSearcher


class TestTarsierSearcher:
    """Test suite for TarsierSearcher."""

    @pytest.fixture
    def mock_browser(self):
        """Mock Browser instance."""
        with patch("tarsier.searcher.Browser") as mock:
            browser = MagicMock()
            mock.return_value = browser
            yield browser

    @pytest.fixture
    def mock_meili_client(self):
        """Mock Meilisearch client."""
        with patch("tarsier.searcher.MeiliClient") as mock:
            client = MagicMock()
            mock.return_value = client
            yield client

    @pytest.fixture
    def mock_qdrant_client(self):
        """Mock Qdrant client."""
        with patch("tarsier.searcher.QdrantClient") as mock:
            client = MagicMock()
            mock.return_value = client
            yield client

    @pytest.fixture
    def searcher(self, mock_browser, mock_meili_client, mock_qdrant_client):
        """Create TarsierSearcher instance with mocked dependencies."""
        return TarsierSearcher()

    def test_init_default_values(self, mock_browser, mock_meili_client, mock_qdrant_client):
        """Test initialization with default values."""
        searcher = TarsierSearcher()
        
        # Check if clients were initialized with default values
        mock_meili_client.assert_called_once_with("http://localhost:7700", None)
        mock_qdrant_client.assert_called_once_with(url="http://localhost:6333", api_key=None)
        
        # Check if browser was initialized without proxy
        mock_browser.assert_called_once_with(proxy=None)

    def test_init_with_proxy(self, mock_browser):
        """Test initialization with proxy configuration."""
        proxy_config = {
            "http": "http://proxy.example.com:8080",
            "https": "http://proxy.example.com:8080"
        }
        
        TarsierSearcher(proxy=proxy_config)
        mock_browser.assert_called_once_with(proxy=proxy_config)

    def test_init_indices(self, mock_meili_client, mock_qdrant_client):
        """Test index initialization."""
        searcher = TarsierSearcher()
        
        # Check if Meilisearch index was created
        mock_meili_client.return_value.get_indexes.return_value = []
        mock_meili_client.return_value.create_index.assert_called_once_with(
            "pages", {"primaryKey": "url"}
        )
        
        # Check if Qdrant collection was created
        mock_qdrant_client.return_value.recreate_collection.assert_called_once_with(
            collection_name="pages",
            vectors_config={"size": 1536, "distance": "Cosine"}
        )

    @patch("tarsier.searcher.extract_text_content")
    @patch("tarsier.searcher.is_pdf_or_image")
    def test_search_process(
        self,
        mock_is_pdf_or_image,
        mock_extract_content,
        searcher,
        mock_browser,
        mock_meili_client,
        mock_qdrant_client
    ):
        """Test search process with mocked content extraction."""
        # Setup mocks
        mock_browser.search_google.return_value = ["http://example.com"]
        mock_is_pdf_or_image.return_value = False
        mock_extract_content.return_value = "Test content"
        
        # Perform search
        results = searcher.search("test query", output_format="text", max_results=1)
        
        # Verify results
        assert len(results) == 1
        assert results[0]["url"] == "http://example.com"
        assert results[0]["content"] == "Test content"
        
        # Verify Meilisearch storage
        mock_meili_client.return_value.index.return_value.add_documents.assert_called_once()
        
        # Verify Qdrant storage
        mock_qdrant_client.return_value.upsert.assert_called_once()

    @patch("tarsier.searcher.extract_text_content")
    @patch("tarsier.searcher.is_pdf_or_image")
    def test_search_error_handling(
        self,
        mock_is_pdf_or_image,
        mock_extract_content,
        searcher,
        mock_browser
    ):
        """Test error handling during search process."""
        # Setup mocks
        mock_browser.search_google.return_value = ["http://example.com"]
        mock_is_pdf_or_image.return_value = False
        mock_extract_content.side_effect = Exception("Test error")
        
        # Perform search
        results = searcher.search("test query")
        
        # Verify that error was handled gracefully
        assert len(results) == 0

    @patch("tarsier.searcher.requests.get")
    @patch("tarsier.searcher.partition")
    def test_extract_content_pdf(
        self,
        mock_partition,
        mock_requests_get,
        searcher,
        mock_browser
    ):
        """Test content extraction from PDF."""
        # Setup mocks
        mock_requests_get.return_value.content = b"PDF content"
        mock_partition.return_value = ["Page 1", "Page 2"]
        
        # Test PDF extraction
        content = searcher._extract_content("http://example.com/doc.pdf", "text")
        
        # Verify content extraction
        assert content == "Page 1\nPage 2"
        mock_requests_get.assert_called_once_with("http://example.com/doc.pdf")
        mock_partition.assert_called_once_with(file=b"PDF content")

    def test_get_embedding(self, searcher):
        """Test embedding generation (placeholder)."""
        # Test placeholder embedding
        embedding = searcher._get_embedding("test text")
        assert len(embedding) == 1536
        assert all(x == 0.0 for x in embedding) 