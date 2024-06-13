import unittest
from unittest.mock import patch, MagicMock
import requests
import pandas as pd

# Importing the functions from the main script
from bollm.billo import get_endpoints, index_rag, query_rag, query_llm, parse_metadata, get_docs_to_index, index_documents

class TestBilloFunctions(unittest.TestCase):

    @patch("requests.post")
    def test_get_endpoints(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'endpoints': [{'name': 'gpt-4'}, {'name': 'gpt-3.5'}]}
        mock_post.return_value = mock_response
        expected_output = ['gpt-4', 'gpt-3.5']
        result = get_endpoints()
        self.assertEqual(result, expected_output)

    @patch("requests.post")
    def test_index_rag(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        documents = ["Document content"]
        metadatas = {"Page": 1, "Source": "Test Source"}
        result = index_rag(documents, metadatas)
        self.assertEqual(result, "Indexed page 1 of Test Source")

    @patch("requests.post")
    def test_query_rag(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': 'some data'}
        mock_post.return_value = mock_response
        result = query_rag("Sample query", 5)
        self.assertEqual(result, {'result': 'some data'})

    @patch("requests.post")
    def test_query_llm(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'choices': [{'text': 'sample response'}]}
        mock_post.return_value = mock_response
        result = query_llm("Sample prompt")
        self.assertEqual(result, {'choices': [{'text': 'sample response'}]})

    def test_parse_metadata(self):
        metadata_str = "key1: value1, key2: value2"
        expected_output = {'key1': 'value1', 'key2': 'value2'}
        result = parse_metadata(metadata_str)
        self.assertEqual(result, expected_output)

    def test_get_docs_to_index(self):
        df = pd.DataFrame({
            "Content": ["Document content"],
            "Metadata": ["key1: value1, key2: value2"]
        })
        expected_documents = ["Document content"]
        expected_metadatas = [{'key1': 'value1', 'key2': 'value2'}]
        documents, metadatas = get_docs_to_index(df)
        self.assertEqual(documents, expected_documents)
        self.assertEqual(metadatas, expected_metadatas)

if __name__ == '__main__':
    unittest.main()
