import unittest
from unittest.mock import patch
import os

# Importing the functions from the main script
from bollm.azure import load_env_variables, load_azure_client, query_llm

class TestAzureFunctions(unittest.TestCase):

    @patch.dict(os.environ, {
        "AZURE_BASE_URL": "https://example.azure.com",
        "AZURE_API_KEY": "test_api_key",
        "AZURE_DEPLOYMENT_NAME": "test_deployment",
        "AZURE_DEPLOYMENT_VERSION": "v1"
    })
    def test_load_env_variables(self):
        config = load_env_variables()
        expected_config = {
            "base_url": "https://example.azure.com",
            "api_key": "test_api_key",
            "deployment_name": "test_deployment",
            "deployment_version": "v1",
            "context_window": 128000
        }
        self.assertEqual(config, expected_config)

    @patch('bollm.azure.openai.AzureOpenAI')
    @patch.dict(os.environ, {
        "AZURE_BASE_URL": "https://example.azure.com",
        "AZURE_API_KEY": "test_api_key",
        "AZURE_DEPLOYMENT_NAME": "test_deployment",
        "AZURE_DEPLOYMENT_VERSION": "v1"
    })
    def test_load_azure_client(self, MockAzureOpenAI):
        config = load_env_variables()
        client = load_azure_client(config)
        MockAzureOpenAI.assert_called_with(
            api_key=config['api_key'],
            api_version=config['deployment_version'],
            azure_endpoint=config['base_url']
        )
        self.assertEqual(client, MockAzureOpenAI())

    @patch('bollm.azure.openai.AzureOpenAI')
    @patch.dict(os.environ, {
        "AZURE_BASE_URL": "https://example.azure.com",
        "AZURE_API_KEY": "test_api_key",
        "AZURE_DEPLOYMENT_NAME": "test_deployment",
        "AZURE_DEPLOYMENT_VERSION": "v1"
    })
    def test_query_llm(self, MockAzureOpenAI):
        mock_client = MockAzureOpenAI()
        mock_response = {"choices": [{"message": {"content": "Test response"}}]}
        mock_client.chat.completions.create.return_value = mock_response
        config = load_env_variables()
        prompt = "Test prompt"
        response = query_llm(config, prompt)
        mock_client.chat.completions.create.assert_called_with(
            model=config['deployment_name'],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=4096
        )
        self.assertEqual(response, mock_response)

if __name__ == '__main__':
    unittest.main()
