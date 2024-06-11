import os

from dotenv import load_dotenv

load_dotenv(os.getcwd() + "/.env")

NOTDIAMOND_API_KEY = os.getenv("NOTDIAMOND_API_KEY", default="")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", default="")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", default="")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", default="")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", default="")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", default="")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", default="")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", default="")


ND_BASE_URL = "https://not-diamond-server.onrender.com"

PROVIDERS = {
    "openai": {
        "models": [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-1106-preview",
            "gpt-4-turbo-preview",
            "gpt-4-turbo-2024-04-09",
            "gpt-4o-2024-05-13",
        ],
        "api_key": OPENAI_API_KEY,
        "support_tools": [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-1106-preview",
            "gpt-4-turbo-preview",
            "gpt-4-turbo-2024-04-09",
            "gpt-4o-2024-05-13",
        ],
        "support_response_model": [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-1106-preview",
            "gpt-4-turbo-preview",
            "gpt-4-turbo-2024-04-09",
            "gpt-4o-2024-05-13",
        ],
        "openrouter_identifier": {
            "gpt-3.5-turbo": "openai/gpt-3.5-turbo",
            "gpt-4": "openai/gpt-4",
            "gpt-4-turbo-preview": "openai/gpt-4-turbo-preview",
            "gpt-4o-2024-05-13": "openai/gpt-4o-2024-05-13",
            "gpt-4-turbo-2024-04-09": "openai/gpt-4-turbo",
        },
    },
    "anthropic": {
        "models": [
            "claude-2.1",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ],
        "api_key": ANTHROPIC_API_KEY,
        "support_tools": [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ],
        "support_response_model": [
            "claude-2.1",
            "claude-3-opus-20240229",
        ],
        "openrouter_identifier": {
            "claude-2.1": "anthropic/claude-2.1",
            "claude-3-opus-20240229": "anthropic/claude-3-opus",
            "claude-3-sonnet-20240229": "anthropic/claude-3-sonnet",
            "claude-3-haiku-20240307": "anthropic/claude-3-haiku",
        },
    },
    "google": {
        "models": [
            "gemini-pro",
            "gemini-1.0-pro-latest",
            "gemini-1.5-pro-latest",
        ],
        "api_key": GOOGLE_API_KEY,
        "support_tools": [
            "gemini-pro",
            "gemini-1.0-pro-latest",
            "gemini-1.5-pro-latest",
        ],
        "support_response_model": [
            "gemini-pro",
            "gemini-1.0-pro-latest",
            "gemini-1.5-pro-latest",
        ],
        "openrouter_identifier": {
            "gemini-pro": "google/gemini-pro",
            "gemini-1.0-pro-latest": "google/gemini-pro",
            "gemini-1.5-pro-latest": "google/gemini-pro-1.5",  #
        },
    },
    "cohere": {
        "models": ["command", "command-r"],
        "api_key": COHERE_API_KEY,
        "support_tools": ["command-r"],
        "support_response_model": ["command", "command-r"],
        "openrouter_identifier": {
            "command": "cohere/command",
            "command-r": "cohere/command-r",
        },
    },
    "mistral": {
        "models": [
            "mistral-large-latest",
            "mistral-medium-latest",
            "mistral-small-latest",
            "open-mistral-7b",
            "open-mixtral-8x7b",
            "open-mixtral-8x22b",
        ],
        "api_key": MISTRAL_API_KEY,
        "support_tools": [
            "mistral-large-latest",
            "mistral-small-latest",
            "open-mixtral-8x22b",
        ],
        "support_response_model": [
            "mistral-large-latest",
            "mistral-medium-latest",
            "mistral-small-latest",
            "open-mistral-7b",
            "open-mixtral-8x7b",
            "open-mixtral-8x22b",
        ],
        "openrouter_identifier": {
            "mistral-large-latest": "mistralai/mistral-large",
            "mistral-medium-latest": "mistralai/mistral-medium",
            "mistral-small-latest": "mistralai/mistral-small",
            "open-mistral-7b": "mistralai/mistral-7b-instruct",
            "open-mixtral-8x7b": "mistralai/mixtral-8x7b",
            "open-mixtral-8x22b": "mistralai/mixtral-8x22b-instruct",
        },
    },
    "togetherai": {
        "models": [
            "CodeLlama-34b-Instruct-hf",
            "Phind-CodeLlama-34B-v2",
            "Mistral-7B-Instruct-v0.2",
            "Mixtral-8x7B-Instruct-v0.1",
            "Mixtral-8x22B-Instruct-v0.1",
            "Llama-3-70b-chat-hf",
            "Llama-3-8b-chat-hf",
        ],
        "api_key": TOGETHER_API_KEY,
        "model_prefix": {
            "CodeLlama-34b-Instruct-hf": "codellama",
            "Phind-CodeLlama-34B-v2": "Phind",
            "Mistral-7B-Instruct-v0.2": "mistralai",
            "Mixtral-8x7B-Instruct-v0.1": "mistralai",
            "Mixtral-8x22B-Instruct-v0.1": "mistralai",
            "Llama-3-70b-chat-hf": "meta-llama",
            "Llama-3-8b-chat-hf": "meta-llama",
        },
        "openrouter_identifier": {
            "Phind-CodeLlama-34B-v2": "phind/phind-codellama-34b",
            "CodeLlama-34b-Instruct-hf": "meta-llama/codellama-34b-instruct",
            "Llama-3-70b-chat-hf": "meta-llama/llama-3-70b-instruct",
            "Llama-3-8b-chat-hf": "meta-llama/llama-3-8b-instruct",
        },
    },
    "perplexity": {
        "models": [
            "llama-3-sonar-large-32k-online",
        ],
        "api_key": PERPLEXITY_API_KEY,
        "openrouter_identifier": {
            "llama-3-sonar-large-32k-online": "perplexity/llama-3-sonar-large-32k-online",
        },
    },
}
