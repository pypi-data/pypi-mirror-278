from . import config
import openai

# Define required environment variables
REQUIRED_VARS = [
    "AZURE_BASE_URL", "AZURE_API_KEY", "AZURE_DEPLOYMENT_VERSION"
]

# Load and validate environment variables
env_vars = config.load_and_validate_env_vars(REQUIRED_VARS)

# Azure API details
BASE_URL = env_vars["AZURE_BASE_URL"]
API_KEY = env_vars["AZURE_API_KEY"]
DEPLOYMENT_VERSION = env_vars["AZURE_DEPLOYMENT_VERSION"]
GPT_4o_CONTEXT_WINDOW = 128000

def load_azure_client(API_KEY, DEPLOYMENT_VERSION, BASE_URL):
    """
    Loads and caches the Azure OpenAI client.

    Returns:
        openai.AzureOpenAI: An instance of the Azure OpenAI client.
    """
    return openai.AzureOpenAI(
        api_key=API_KEY,
        api_version=DEPLOYMENT_VERSION,
        azure_endpoint=BASE_URL
    )

def query_llm(prompt, model_type, max_tokens=4096, temperature=0.0):
    """
    Queries the Azure OpenAI language model with the given prompt.

    Args:
        config (dict): A dictionary containing the configuration details.
        prompt (str): The prompt to send to the language model.
        model_type (str): The deployment name in your Azure model deployments.
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 4096.
        temperature (float, optional): The sampling temperature. Defaults to 0.0.

    Returns:
        dict: The response from the language model.
    """
    client = load_azure_client(API_KEY, DEPLOYMENT_VERSION, BASE_URL)
    response = client.chat.completions.create(
        model=model_type,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response

def get_content(response_full):
    return response_full.choices[0].message.content

def get_token_usage(response_full):
    return response_full.usage.total_tokens