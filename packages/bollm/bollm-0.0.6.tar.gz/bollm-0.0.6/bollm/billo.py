
import requests
from concurrent.futures import ThreadPoolExecutor
from . import config

# Define required environment variables
REQUIRED_VARS = [
    "BILLO_BASE_URL", "BILLO_API_KEY",
    "BILLO_USER_ID", "VERIFY_SSL_CERT"
]

# Load and validate environment variables
env_vars = config.load_and_validate_env_vars(REQUIRED_VARS)

# BILLO API details
BASE_URL = env_vars["BILLO_BASE_URL"]
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-api-key': env_vars["BILLO_API_KEY"],
}
EMBEDDING_MODEL = "azure-embeddings"
GPT_4_CONTEXT_WINDOW = 8000
VERIFY_SSL_CERT = env_vars["VERIFY_SSL_CERT"]

def get_endpoints():
    """
    Retrieves available endpoints from the BILLO API.

    Returns:
        list: List of available endpoints.

    Example:
        endpoints = get_endpoints()
        print(endpoints)
    """
    response = requests.post(BASE_URL + "/api/2.0/endpoints", headers=HEADERS, verify=VERIFY_SSL_CERT)
    response.raise_for_status()
    return [endpoint['name'] for endpoint in response.json()['endpoints'] if endpoint['name'] in ["gpt-4", "gpt-3.5", "claude-instant", "claude-2-1", "claude-2-0"]] # these are the only ones that appear to work

def query_rag(user_query, num_chunks, index_name):
    """
    Queries the RAG system with a user query.

    Args:
        user_query (str): The query to send to the RAG system.
        num_chunks (int): Number of chunks to retrieve.

    Returns:
        dict: The response from the RAG system.

    Example:
        response = query_rag("What is the capital of France?", 5)
        print(response)
    """
    json_data = {
        "index_name": index_name,
        "embedding_model": "azure-embeddings",
        "query": user_query,
        "num_neighbors": num_chunks
    }
    response = requests.post(BASE_URL + "/rag/query", headers=HEADERS, json=json_data, verify=VERIFY_SSL_CERT)
    response.raise_for_status()
    return response.json()

def query_llm(prompt, model_type="gpt-4", max_tokens=64, temperature=0.0):
    """
    Queries the LLM with a given prompt.

    Args:
        prompt (str): The prompt to send to the LLM.
        model_type (str, optional): The model type to use. Defaults to "gpt-4".
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 64.
        temperature (float, optional): The sampling temperature. Defaults to 0.0.

    Returns:
        dict: The response from the LLM.

    Example:
        response = query_llm("Tell me a joke.")
        print(response)
    """
    json_data = {
        "max_tokens": max_tokens,
        "n": 1,
        "prompt": prompt,
        "stop": ["END"],
        "temperature": temperature
    }
    response = requests.post(BASE_URL + f'/endpoints/{model_type}/invocations', headers=HEADERS, json=json_data, verify=VERIFY_SSL_CERT)
    response.raise_for_status()
    return response.json()

def separate_for_indexing(processed_docs):
    """
    Prepares documents and metadata for indexing.

    Args:
        processed_docs (pd.DataFrame): DataFrame containing document data.

    Returns:
        tuple: Tuple containing lists of documents ids, and metadata.

    Example:
        documents, ids, metadata = separate_for_indexing(processed_docs)
        print(documents, ids, metadata)
    """
    documents = processed_docs[['Content']].apply(lambda x: ' '.join(x.dropna().values.tolist()), axis=1).tolist() 
    ids = processed_docs[['Chunk_ID']].apply(lambda x: ' '.join(x.dropna().values.tolist()), axis=1).tolist()
    metadata = processed_docs["Metadata"].tolist()
    return documents, ids, metadata

def index_rag_multi_threaded(documents, metadata, index_name, max_workers=8):
    """
    Indexes documents using a thread pool.

    Args:
        documents (list): List of documents to index.
        metadatas (list): List of metadata associated with documents.

    Example:
        index_documents(documents, metadatas)
    """
    index_name = [index_name] * len(documents)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for result in executor.map(_index_rag, documents, metadata, index_name):
            if result:
                print(result)


def _index_rag(documents, metadata, index_name):
    """
    Indexes documents and metadata to the RAG system.

    Args:
        documents (list): List of documents to index.
        metadata (list): List of metadata associated with documents.

    Returns:
        str: Status message of the indexing process.

    Example:
        status = index_rag(documents, metadatas)
        print(status)
    """
    json_data = {
        "index_name": index_name,
        "embedding_model": EMBEDDING_MODEL,
        "texts": [documents],
        "metadatas": [metadata]
    }
    try:
        response = requests.post(BASE_URL + "/rag/index", headers=HEADERS, json=json_data, verify=VERIFY_SSL_CERT)
        response.raise_for_status()
        return f"Indexed a chunk on page {metadata['Page']} of {metadata['Source']}"
    except Exception as e:
        print('Request failed due to error:', e)
        return None

def get_content(response_full):
    return response_full['choices'][0]['text']

def get_token_usage(response_full):
    return response_full["usage"]["total_tokens"]