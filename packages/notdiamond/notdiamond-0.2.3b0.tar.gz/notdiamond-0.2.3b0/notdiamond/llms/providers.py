from enum import Enum

from notdiamond.llms.provider import NDLLMProvider


class NDLLMProviders(Enum):
    """
    NDLLMProviders serves as a registry for the supported LLM models by NotDiamond.
    It allows developers to easily specify available LLM providers for the router.

    Attributes:
        GPT_3_5_TURBO (NDLLMProvider): refers to 'gpt-3.5-turbo' model by OpenAI
        GPT_4 (NDLLMProvider): refers to 'gpt-4' model by OpenAI
        GPT_4_1106_PREVIEW (NDLLMProvider): refers to 'gpt-4-1106-preview' model by OpenAI
        GPT_4_TURBO_PREVIEW (NDLLMProvider): refers to 'gpt-4-turbo-preview' model by OpenAI
        GPT_4_TURBO_2024_04_09 (NDLLMProvider): refers to 'gpt-4-turbo-2024-04-09' model by OpenAI
        GPT_4o_2024_05_13 (NDLLMProvider): refers to 'gpt-4o-2024-05-13' model by OpenAI
        CLAUDE_2_1 (NDLLMProvider): refers to 'claude-2.1' model by Anthropic
        CLAUDE_3_OPUS_20240229 (NDLLMProvider): refers to 'claude-3-opus-20240229' model by Anthropic
        CLAUDE_3_SONNET_20240229 (NDLLMProvider): refers to 'claude-3-sonnet-20240229' model by Anthropic
        CLAUDE_3_HAIKU_20240307 (NDLLMProvider): refers to 'claude-3-haiku-20240307' model by Anthropic
        GEMINI_PRO (NDLLMProvider): refers to 'gemini-pro' model by Google
        GEMINI_1_PRO_LATEST (NDLLMProvider): refers to 'gemini-1.0-pro-latest' model by Google
        GEMINI_15_PRO_LATEST (NDLLMProvider): refers to 'gemini-1.5-pro-latest' model by Google
        COMMAND (NDLLMProvider): refers to 'command' model by Cohere
        COMMAND_R (NDLLMProvider): refers to 'command-r' model by Cohere
        MISTRAL_LARGE_LATEST (NDLLMProvider): refers to 'mistral-large-latest' model by Mistral AI
        MISTRAL_MEDIUM_LATEST (NDLLMProvider): refers to 'mistral-medium-latest' model by Mistral AI
        MISTRAL_SMALL_LATEST (NDLLMProvider): refers to 'mistral-small-latest' model by Mistral AI
        OPEN_MISTRAL_7B (NDLLMProvider): refers to 'open-mistral-7b' model by Mistral AI
        OPEN_MIXTRAL_8X7B (NDLLMProvider): refers to 'open-mixtral-8x7b' model by Mistral AI
        OPEN_MIXTRAL_8X22B (NDLLMProvider): refers to 'open-mixtral-8x22b' model by Mistral AI
        CODELLAMA_34B_INSTRUCT_HF (NDLLMProvider): refers to 'CodeLlama-34b-Instruct-hf' model served via TogetherAI
        PHIND_CODELLAMA_34B_V2 (NDLLMProvider): refers to 'Phind-CodeLlama-34B-v2' model served via TogetherAI
        MISTRAL_7B_INSTRUCT_V0_2 (NDLLMProvider): refers to 'Mistral-7B-Instruct-v0.2' model served via TogetherAI
        MIXTRAL_8X7B_INSTRUCT_V0_1 (NDLLMProvider): refers to 'Mixtral-8x7B-Instruct-v0.1' model served via TogetherAI
        MIXTRAL_8X22B_INSTRUCT_V0_1 (NDLLMProvider): refers to 'Mixtral-8x22B-Instruct-v0.1' model served via TogetherAI

    Note:
        This class is static and designed to be used without instantiation.
        Access its attributes directly to obtain configurations for specific LLM providers.
    """

    GPT_3_5_TURBO = ("openai", "gpt-3.5-turbo")
    GPT_4 = ("openai", "gpt-4")
    GPT_4_1106_PREVIEW = ("openai", "gpt-4-1106-preview")
    GPT_4_TURBO_PREVIEW = ("openai", "gpt-4-turbo-preview")
    GPT_4_TURBO_2024_04_09 = ("openai", "gpt-4-turbo-2024-04-09")
    GPT_4o_2024_05_13 = ("openai", "gpt-4o-2024-05-13")
    CLAUDE_2_1 = ("anthropic", "claude-2.1")
    CLAUDE_3_OPUS_20240229 = ("anthropic", "claude-3-opus-20240229")
    CLAUDE_3_SONNET_20240229 = ("anthropic", "claude-3-sonnet-20240229")
    CLAUDE_3_HAIKU_20240307 = ("anthropic", "claude-3-haiku-20240307")
    GEMINI_PRO = ("google", "gemini-pro")
    GEMINI_1_PRO_LATEST = ("google", "gemini-1.0-pro-latest")
    GEMINI_15_PRO_LATEST = ("google", "gemini-1.5-pro-latest")
    COMMAND = ("cohere", "command")
    COMMAND_R = ("cohere", "command-r")
    MISTRAL_LARGE_LATEST = ("mistral", "mistral-large-latest")
    MISTRAL_MEDIUM_LATEST = ("mistral", "mistral-medium-latest")
    MISTRAL_SMALL_LATEST = ("mistral", "mistral-small-latest")
    OPEN_MISTRAL_7B = ("mistral", "open-mistral-7b")
    OPEN_MIXTRAL_8X7B = ("mistral", "open-mixtral-8x7b")
    OPEN_MIXTRAL_8X22B = ("mistral", "open-mixtral-8x22b")
    CODELLAMA_34B_INSTRUCT_HF = ("togetherai", "CodeLlama-34b-Instruct-hf")
    PHIND_CODELLAMA_34B_V2 = ("togetherai", "Phind-CodeLlama-34B-v2")
    MISTRAL_7B_INSTRUCT_V0_2 = ("togetherai", "Mistral-7B-Instruct-v0.2")
    MIXTRAL_8X7B_INSTRUCT_V0_1 = ("togetherai", "Mixtral-8x7B-Instruct-v0.1")
    MIXTRAL_8X22B_INSTRUCT_V0_1 = ("togetherai", "Mixtral-8x22B-Instruct-v0.1")
    LLAMA_3_70B_CHAT_HF = ("togetherai", "Llama-3-70b-chat-hf")
    LLAMA_3_8B_CHAT_HF = ("togetherai", "Llama-3-8b-chat-hf")
    LLAMA_3_SONAR_LARGE_32K_ONLINE = (
        "perplexity",
        "llama-3-sonar-large-32k-online",
    )

    def __new__(cls, provider, model):
        return NDLLMProvider(provider=provider, model=model)
