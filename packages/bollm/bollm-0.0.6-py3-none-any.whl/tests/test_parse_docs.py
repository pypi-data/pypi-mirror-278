import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd

# Importing the functions from the main script
from bollm.parse_docs import get_filenames, split_pdf_pages_with_metadata, create_chunks_with_unique_ids, store_processed_files_to_parquet

class TestParseDocsFunctions(unittest.TestCase):

    @patch("os.listdir")
    @patch("os.path.isfile")
    def test_get_filenames(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.pdf', 'file2.pdf']
        mock_isfile.return_value = True
        directory = '/path/to/directory'
        expected_output = pd.DataFrame([
            {"name": "file1.pdf", "path": "/path/to/directory/file1.pdf"},
            {"name": "file2.pdf", "path": "/path/to/directory/file2.pdf"}
        ])
        result = get_filenames(directory)
        pd.testing.assert_frame_equal(result, expected_output)

    @patch("bollm.parse_docs.UnstructuredFileLoader")
    def test_split_pdf_pages_with_metadata(self, MockUnstructuredFileLoader):
        mock_loader_instance = MockUnstructuredFileLoader.return_value
        mock_loader_instance.load.return_value = [
            MagicMock(page_content="Page content", metadata={"last_modified": "2023-01-01"})
        ]
        file_path = '/path/to/file.pdf'
        ID_name = 'file_id'
        expected_output = pd.DataFrame([
            {"ID": "file_id 1", "Content": "Page content", "Source": "file_id", "Metadata": "2023-01-01"}
        ])
        result = split_pdf_pages_with_metadata(file_path, ID_name)
        pd.testing.assert_frame_equal(result, expected_output)

    @patch("bollm.parse_docs.RecursiveCharacterTextSplitter")
    def test_create_chunks_with_unique_ids(self, MockTextSplitter):
        mock_text_splitter = MockTextSplitter.return_value
        mock_text_splitter.split_text.return_value = ["Chunk 1", "Chunk 2"]
        doc_df = pd.DataFrame([
            {"ID": "doc1", "Content": "Some long content", "Metadata": "meta1"}
        ])
        expected_output = pd.DataFrame([
            {'Chunk_ID': 'doc1 - Chunk 1', 'Content': 'Chunk 1', 'Metadata': 'meta1'},
            {'Chunk_ID': 'doc1 - Chunk 2', 'Content': 'Chunk 2', 'Metadata': 'meta1'}
        ])
        result = create_chunks_with_unique_ids(doc_df, mock_text_splitter)
        pd.testing.assert_frame_equal(result, expected_output)

    @patch("bollm.parse_docs.split_pdf_pages_with_metadata")
    @patch("bollm.parse_docs.group_broken_paragraphs")
    @patch("bollm.parse_docs.create_chunks_with_unique_ids")
    @patch("bollm.parse_docs.RecursiveCharacterTextSplitter")
    def test_store_processed_files_to_parquet(self, MockTextSplitter, mock_create_chunks, mock_group_broken_paragraphs, mock_split_pdf):
        mock_split_pdf.return_value = pd.DataFrame([
            {"ID": "file_id 1", "Content": "Page content", "Source": "file_id", "Metadata": "2023-01-01"}
        ])
        mock_group_broken_paragraphs.side_effect = lambda x: x
        mock_create_chunks.return_value = pd.DataFrame([
            {'Chunk_ID': 'file_id 1 - Chunk 1', 'Content': 'Chunk content', 'Metadata': '2023-01-01'}
        ])
        filenames = pd.DataFrame([
            {"name": "file1.pdf", "path": "/path/to/file1.pdf"}
        ])
        expected_output = pd.DataFrame([
            {'Chunk_ID': 'file_id 1 - Chunk 1', 'Content': 'Chunk content', 'Metadata': '2023-01-01'}
        ])
        result = store_processed_files_to_parquet(filenames)
        pd.testing.assert_frame_equal(result, expected_output)

if __name__ == '__main__':
    unittest.main()
