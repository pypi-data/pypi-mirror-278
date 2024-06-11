"""NDLLM Class"""

import time
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Type,
    Union,
)

from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_cohere.chat_models import ChatCohere
from langchain_community.chat_models import ChatPerplexity
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.messages import AIMessage, BaseMessage, BaseMessageChunk
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompt_values import StringPromptValue
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_openai import ChatOpenAI
from langchain_together import Together
from litellm import token_counter
from pydantic import BaseModel
from pydantic_partial import create_partial_model

from notdiamond import settings
from notdiamond.callbacks import NDLLMBaseCallbackHandler
from notdiamond.exceptions import ApiError, MissingLLMProviders
from notdiamond.llms.provider import NDLLMProvider
from notdiamond.llms.request import amodel_select, model_select, report_latency
from notdiamond.metrics.metric import NDMetric
from notdiamond.prompts.prompt import NDChatPromptTemplate, NDPromptTemplate
from notdiamond.types import NDApiKeyValidator


class NDLLM(LLM):
    """
    Implementation of NDLLM class, the main class responsible for routing.
    The class inherits from Langchain's LLM class. Starting reference is from here:
    https://python.langchain.com/docs/modules/model_io/llms/custom_llm

    It's mandatory to have an API key set. If the api_key is not explicitly specified,
    it will check for NOTDIAMOND_API_KEY in the .env file.

    Raises:
        MissingLLMProviders: you must specify at least one LLM provider for the router to work
        ApiError: error raised when the NotDiamond API call fails.
                    Ensure to set a default LLM provider to not break the code.
    """

    api_key: str
    """
    API key required for making calls to NotDiamond.
    You can get an API key via our dashboard: https://app.notdiamond.ai
    If an API key is not set, it will check for NOTDIAMOND_API_KEY in .env file.
    """

    llm_providers: Optional[List[NDLLMProvider]]
    """The list of LLM providers that are available to route between."""

    default: Union[NDLLMProvider, int, str]
    """
    Set a default LLM provider, so in case anything goes wrong in the flow,
    as for example NotDiamond API call fails, your code won't break and you have
    a fallback model. There are various ways to configure a default model:

    - Integer, specifying the index of the default provider from the llm_providers list
    - String, similar how you can specify llm_providers, of structure 'provider_name/model_name'
    - NDLLMProvider, just directly specify the object of the provider

    By default, we will set your first LLM in the list as the default.
    """

    max_model_depth: Optional[int]
    """
    If your top recommended model is down, specify up to which depth of routing you're willing to go.
    If max_model_depth is not set, it defaults to the length of the llm_providers list.
    If max_model_depth is set to 0, the init will fail.
    If the value is larger than the llm_providers list length, we reset the value to len(llm_providers).
    """

    latency_tracking: bool
    """
    Tracking and sending latency of LLM call to NotDiamond server as feedback, so we can improve our router.
    By default this is turned on, set it to False to turn off.
    """

    hash_content: bool
    """
    Hashing the content before being sent to the NotDiamond API.
    By default this is False.
    """

    tradeoff: Optional[str]
    """
    Define tradeoff between "cost" and "latency" for the router to determine the best LLM for a given query.
    If None is specified, then the router will not consider either cost or latency.

    The supported values: "cost", "latency"

    Defaults to None.
    """

    preference_id: Optional[str]
    """The ID of the router preference that was configured via the Dashboard. Defaults to None."""

    tools: Optional[Sequence[Union[Dict[str, Any], Callable]]]
    """Bind tools to the LLM object. The tools will be passed to the LLM object when invoking it."""

    callbacks: Optional[
        List[Union[BaseCallbackHandler, NDLLMBaseCallbackHandler]]
    ]
    """
    Callback handler for the LLM object. It will be passed to the LLM object when invoking it.
    Also has custom NDLLM callbacks:
    - on_model_select
    - on_latency_tracking
    - on_api_error
    """

    def __init__(
        self,
        llm_providers: Optional[List[NDLLMProvider]] = None,
        api_key: Optional[str] = None,
        default: Union[NDLLMProvider, int, str] = 0,
        max_model_depth: Optional[int] = None,
        latency_tracking: bool = True,
        hash_content: bool = False,
        tradeoff: Optional[str] = None,
        preference_id: Optional[str] = None,
        callbacks: Optional[
            List[Union[BaseCallbackHandler, NDLLMBaseCallbackHandler]]
        ] = None,
        **kwargs,
    ) -> None:
        if api_key is None:
            api_key = settings.NOTDIAMOND_API_KEY
        NDApiKeyValidator(api_key=api_key)

        if llm_providers is not None:
            llm_providers = self._parse_llm_providers_data(llm_providers)

            if max_model_depth is None:
                max_model_depth = len(llm_providers)

            if max_model_depth > len(llm_providers):
                print(
                    "WARNING: max_model_depth cannot be bigger than the number of LLM providers."
                )
                max_model_depth = len(llm_providers)

        if tradeoff is not None:
            if tradeoff not in ["cost", "latency"]:
                raise ValueError(
                    "Invalid tradeoff. Accepted values: cost, latency."
                )

        super(NDLLM, self).__init__(
            api_key=api_key,
            llm_providers=llm_providers,
            default=default,
            max_model_depth=max_model_depth,
            latency_tracking=latency_tracking,
            hash_content=hash_content,
            tradeoff=tradeoff,
            preference_id=preference_id,
            callbacks=callbacks,
            **kwargs,
        )

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        address = hex(id(self))  # Gets the memory address of the object
        return f"<{class_name} object at {address}>"

    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    @property
    def default_llm_provider(self) -> Union[NDLLMProvider, None]:
        """
        Return the default LLM provider that's set on the NDLLM class.
        """
        if isinstance(self.default, int):
            return self.llm_providers[int(self.default)]
        if isinstance(self.default, str):
            if self.default.isdigit():
                return self.llm_providers[int(self.default)]
            return NDLLMProvider.from_string(self.default)
        if isinstance(self.default, NDLLMProvider):
            return self.default
        return self.llm_providers[0]

    @staticmethod
    def _parse_llm_providers_data(llm_providers: list) -> List[NDLLMProvider]:
        providers = []
        for llm_provider in llm_providers:
            if isinstance(llm_provider, NDLLMProvider):
                providers.append(llm_provider)
                continue
            parsed_provider = NDLLMProvider.from_string(llm_provider)
            providers.append(parsed_provider)
        return providers

    @property
    def _llm_type(self) -> str:
        return "NotDiamond LLM"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return "This function is deprecated for the latest LangChain version, use invoke instead"

    def create(
        self,
        messages: List[Dict[str, str]],
        model: Optional[List[NDLLMProvider]] = None,
        default: Optional[Union[NDLLMProvider, int, str]] = None,
        max_model_depth: Optional[int] = None,
        latency_tracking: Optional[bool] = None,
        hash_content: Optional[bool] = None,
        tradeoff: Optional[str] = None,
        preference_id: Optional[str] = None,
        metric: NDMetric = NDMetric("accuracy"),
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> tuple[Union[AIMessage, BaseModel], str, NDLLMProvider]:
        """
        Function call to invoke the LLM, with the same interface
        as the OpenAI Python library.

        Parameters:
            messages (Optional[List[Dict[str, str]], optional): Can be used instead of prompt_template to pass
                the messages OpenAI style.
            model (Optional[List[NDLLMProvider]]): List of models to choose from.
            default (Optional[Union[NDLLMProvider, int, str]]): Default LLM provider.
            max_model_depth (Optional[int]): If your top recommended model is down, specify up to which depth
                                                of routing you're willing to go.
            latency_tracking (Optional[bool]): Latency tracking flag.
            hash_content (Optional[bool]): Flag for hashing content before sending to NotDiamond API.
            tradeoff (Optional[str], optional): Define the "cost" or "latency" tradeoff
                                                for the router to determine the best LLM for a given query.
            preference_id (Optional[str]): The ID of the router preference that was configured via the Dashboard.
                                            Defaults to None.
            **kwargs: Any other arguments that are supported by Langchain's invoke method, will be passed through.

        Raises:
            ApiError: when the NotDiamond API fails

        Returns:
            tuple[Union[AIMessage, BaseModel], str, NDLLMProvider]:
                result: response type defined by Langchain, contains the response from the LLM.
                or object of the response_model
                str: session_id returned by the NotDiamond API
                NDLLMProvider: the best LLM provider selected by the router
        """

        if model is not None:
            llm_providers = self._parse_llm_providers_data(model)
            self.llm_providers = llm_providers

        self.validate_params(
            default=default,
            max_model_depth=max_model_depth,
            latency_tracking=latency_tracking,
            hash_content=hash_content,
            tradeoff=tradeoff,
            preference_id=preference_id,
        )

        return self.invoke(
            messages=messages,
            metric=metric,
            response_model=response_model,
            **kwargs,
        )

    async def acreate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[List[NDLLMProvider]] = None,
        default: Optional[Union[NDLLMProvider, int, str]] = None,
        max_model_depth: Optional[int] = None,
        latency_tracking: Optional[bool] = None,
        hash_content: Optional[bool] = None,
        tradeoff: Optional[str] = None,
        preference_id: Optional[str] = None,
        metric: NDMetric = NDMetric("accuracy"),
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> tuple[Union[AIMessage, BaseModel], str, NDLLMProvider]:
        """
        Async function call to invoke the LLM, with the same interface
        as the OpenAI Python library.

        Parameters:
            messages (Optional[List[Dict[str, str]], optional): Can be used instead of prompt_template to pass
                the messages OpenAI style.
            model (Optional[List[NDLLMProvider]]): List of models to choose from.
            default (Optional[Union[NDLLMProvider, int, str]]): Default LLM provider.
            max_model_depth (Optional[int]): If your top recommended model is down, specify up to which depth
                                                of routing you're willing to go.
            latency_tracking (Optional[bool]): Latency tracking flag.
            hash_content (Optional[bool]): Flag for hashing content before sending to NotDiamond API.
            tradeoff (Optional[str], optional): Define the "cost" or "latency" tradeoff
                                                for the router to determine the best LLM for a given query.
            preference_id (Optional[str]): The ID of the router preference that was configured via the Dashboard.
                                            Defaults to None.
            **kwargs: Any other arguments that are supported by Langchain's invoke method, will be passed through.

        Raises:
            ApiError: when the NotDiamond API fails

        Returns:
            tuple[Union[AIMessage, BaseModel], str, NDLLMProvider]:
                result: response type defined by Langchain, contains the response from the LLM.
                or object of the response_model
                str: session_id returned by the NotDiamond API
                NDLLMProvider: the best LLM provider selected by the router
        """
        if model is not None and len(model) > 0:
            llm_providers = self._parse_llm_providers_data(model)
            self.llm_providers = llm_providers

        self.validate_params(
            default=default,
            max_model_depth=max_model_depth,
            latency_tracking=latency_tracking,
            hash_content=hash_content,
            tradeoff=tradeoff,
            preference_id=preference_id,
        )

        result = await self.ainvoke(
            messages=messages,
            metric=metric,
            response_model=response_model,
            **kwargs,
        )
        return result

    def invoke(
        self,
        prompt_template: Optional[
            Union[
                NDPromptTemplate,
                PromptTemplate,
                NDChatPromptTemplate,
                ChatPromptTemplate,
                str,
            ]
        ] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        input: Optional[Dict[str, Any]] = None,
        metric: NDMetric = NDMetric("accuracy"),
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> tuple[Union[AIMessage, BaseModel], str, NDLLMProvider]:
        """
        Function to invoke the LLM. Behind the scenes what happens:
        1. API call to NotDiamond backend to get the most suitable LLM for the given prompt
        2. Invoke the returned LLM client side
        3. Return the response

        Parameters:
            prompt_template (Optional(Union[ NDPromptTemplate, PromptTemplate, NDChatPromptTemplate, ChatPromptTemplate, str, ])):
                the prompt template defined by the user. It also supports Langchain prompt template types.
            messages (Optional[List[Dict[str, str]], optional): Can be used instead of prompt_template to pass
                the messages OpenAI style.
            input (Optional[Dict[str, Any]], optional): If the prompt_template contains variables, use input to specify
                                                        the values for those variables. Defaults to None, assuming no variables.
            metric (NDMetric, optional): Metric used by NotDiamond router to choose the best LLM.
                                            Defaults to NDMetric("accuracy").
            response_model (Optional[Type[BaseModel]], optional): If present, will use JsonOutputParser to parse the response into
                                                              the given model. In which case result will a dict.
            **kwargs: Any other arguments that are supported by Langchain's invoke method, will be passed through.

        Raises:
            ApiError: when the NotDiamond API fails

        Returns:
            tuple[Union[AIMessage, BaseModel], str, NDLLMProvider]:
                result: response type defined by Langchain, contains the response from the LLM.
                or object of the response_model
                str: session_id returned by the NotDiamond API
                NDLLMProvider: the best LLM provider selected by the router
        """

        # If response_model is present, we will parse the response into the given model
        # doing this here so that if validation errors occur, we can raise them before making the API call
        response_model_parser = None
        if response_model is not None:
            self.verify_against_response_model()
            response_model_parser = JsonOutputParser(
                pydantic_object=response_model
            )

        prompt_template = self._prepare_prompt_template(
            prompt_template,
            messages,
            response_model_parser=response_model_parser,
        )

        if input is None:
            input = {}

        prompt_template.partial_variables = {
            **prompt_template.partial_variables,
            **input,
        }

        best_llm, session_id = model_select(
            prompt_template=prompt_template,
            llm_providers=self.llm_providers,
            metric=metric,
            notdiamond_api_key=self.api_key,
            max_model_depth=self.max_model_depth,
            hash_content=self.hash_content,
            tradeoff=self.tradeoff,
            preference_id=self.preference_id,
            tools=self.tools,
        )

        is_default = False
        if not best_llm:
            best_llm = self.default_llm_provider
            is_default = True

            if best_llm is None:
                error_message = (
                    "ND couldn't find a suitable model to call."
                    + "To avoid disruptions, we recommend setting a default fallback model or increasing max model depth."
                )
                self.call_callbacks("on_api_error", error_message)
                raise ApiError(error_message)
        self.call_callbacks("on_model_select", best_llm, best_llm.model)

        llm = self._llm_from_provider(best_llm, callbacks=self.callbacks)

        if self.tools:
            llm = llm.bind_tools(self.tools)

        chain = prompt_template | llm

        try:
            if self.latency_tracking:
                result = self._invoke_with_latency_tracking(
                    session_id=session_id,
                    chain=chain,
                    llm_provider=best_llm,
                    is_default=is_default,
                    input=input,
                    **kwargs,
                )
            else:
                result = chain.invoke(input, **kwargs)
        except (ChatGoogleGenerativeAIError, ValueError) as e:
            if (
                isinstance(prompt_template, NDChatPromptTemplate)
                and best_llm.provider == "google"
            ):
                print(
                    f"WARNING: Google model's chat messages are violating requirements with error {e}."
                )
                print(
                    "If you see this message, means the NotDiamond API returned a Google model as the best option,"
                    + "but the LLM call will fail. So we will automatically fall back to a non-Google model, if possible."
                )

                non_google_llm = next(
                    (
                        llm_provider
                        for llm_provider in self.llm_providers
                        if llm_provider.provider != "google"
                    ),
                    None,
                )

                if non_google_llm is not None:
                    best_llm = non_google_llm
                    llm = self._llm_from_provider(
                        best_llm, callbacks=self.callbacks
                    )
                    chain = prompt_template | llm

                    if self.latency_tracking:
                        result = self._invoke_with_latency_tracking(
                            session_id=session_id,
                            chain=chain,
                            llm_provider=best_llm,
                            is_default=is_default,
                            input=input,
                            **kwargs,
                        )
                    else:
                        result = chain.invoke(input, **kwargs)
                else:
                    raise e
            else:
                raise e

        if isinstance(result, str):
            result = AIMessage(content=result)

        if response_model is not None:
            parsed_dict = response_model_parser.parse(result.content)
            result = response_model.parse_obj(parsed_dict)

        return result, session_id, best_llm

    async def ainvoke(
        self,
        prompt_template: Optional[
            Union[
                NDPromptTemplate,
                PromptTemplate,
                NDChatPromptTemplate,
                ChatPromptTemplate,
                str,
            ]
        ] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        input: Optional[Dict[str, Any]] = None,
        metric: NDMetric = NDMetric("accuracy"),
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> tuple[Union[AIMessage, BaseModel], str, NDLLMProvider]:
        """
        Function to invoke the LLM. Behind the scenes what happens:
        1. API call to NotDiamond backend to get the most suitable LLM for the given prompt
        2. Invoke the returned LLM client side
        3. Return the response

        Parameters:
            prompt_template (Optional(Union[ NDPromptTemplate, PromptTemplate, NDChatPromptTemplate, ChatPromptTemplate, str, ])):
                the prompt template defined by the user. It also supports Langchain prompt template types.
            messages (Optional[List[Dict[str, str]], optional): Can be used instead of prompt_template to pass
                the messages OpenAI style.
            input (Optional[Dict[str, Any]], optional): If the prompt_template contains variables, use input to specify
                                                        the values for those variables. Defaults to None, assuming no variables.
            metric (NDMetric, optional): Metric used by NotDiamond router to choose the best LLM.
                                            Defaults to NDMetric("accuracy").
            response_model (Optional[Type[BaseModel]], optional): If present, will use JsonOutputParser to parse the response into
                                                              the given model. In which case result will a dict.
            **kwargs: Any other arguments that are supported by Langchain's invoke method, will be passed through.

        Raises:
            ApiError: when the NotDiamond API fails

        Returns:
            tuple[Union[AIMessage, BaseModel], str, NDLLMProvider]:
                result: response type defined by Langchain, contains the response from the LLM.
                or object of the response_model
                str: session_id returned by the NotDiamond API
                NDLLMProvider: the best LLM provider selected by the router
        """

        response_model_parser = None
        if response_model is not None:
            self.verify_against_response_model()
            response_model_parser = JsonOutputParser(
                pydantic_object=response_model
            )

        prompt_template = self._prepare_prompt_template(
            prompt_template,
            messages,
            response_model_parser=response_model_parser,
        )

        if input is None:
            input = {}

        prompt_template.partial_variables = {
            **prompt_template.partial_variables,
            **input,
        }

        best_llm, session_id = await amodel_select(
            prompt_template=prompt_template,
            llm_providers=self.llm_providers,
            metric=metric,
            notdiamond_api_key=self.api_key,
            max_model_depth=self.max_model_depth,
            hash_content=self.hash_content,
            tradeoff=self.tradeoff,
            preference_id=self.preference_id,
            tools=self.tools,
        )

        is_default = False
        if not best_llm:
            best_llm = self.default_llm_provider
            is_default = True

            if best_llm is None:
                error_message = (
                    "ND couldn't find a suitable model to call."
                    + "To avoid disruptions, we recommend setting a default fallback model or make max depth larger."
                )
                self.call_callbacks("on_api_error", error_message)
                raise ApiError(error_message)
        self.call_callbacks("on_model_select", best_llm, best_llm.model)

        llm = self._llm_from_provider(best_llm, callbacks=self.callbacks)

        if self.tools:
            llm = llm.bind_tools(self.tools)

        chain = prompt_template | llm

        try:
            if self.latency_tracking:
                result = await self._async_invoke_with_latency_tracking(
                    session_id=session_id,
                    chain=chain,
                    llm_provider=best_llm,
                    is_default=is_default,
                    input=input,
                    **kwargs,
                )
            else:
                result = await chain.ainvoke(input, **kwargs)
        except (ChatGoogleGenerativeAIError, ValueError) as e:
            if (
                isinstance(prompt_template, NDChatPromptTemplate)
                and best_llm.provider == "google"
            ):
                print(
                    f"WARNING: Google model's chat messages are violating requirements with error {e}."
                )
                print(
                    "If you see this message, means the NotDiamond API returned a Google model as the best option,"
                    + "but the LLM call will fail. So we will automatically fall back to a non-Google model, if possible."
                )

                non_google_llm = next(
                    (
                        llm_provider
                        for llm_provider in self.llm_providers
                        if llm_provider.provider != "google"
                    ),
                    None,
                )

                if non_google_llm is not None:
                    best_llm = non_google_llm
                    llm = self._llm_from_provider(
                        best_llm, callbacks=self.callbacks
                    )
                    chain = prompt_template | llm

                    if self.latency_tracking:
                        result = (
                            await self._async_invoke_with_latency_tracking(
                                session_id=session_id,
                                chain=chain,
                                llm_provider=best_llm,
                                is_default=is_default,
                                input=input,
                                **kwargs,
                            )
                        )
                    else:
                        result = await chain.ainvoke(input, **kwargs)
                else:
                    raise e
            else:
                raise e

        if isinstance(result, str):
            result = AIMessage(content=result)

        if response_model is not None:
            parsed_dict = response_model_parser.parse(result.content)
            result = response_model.parse_obj(parsed_dict)

        return result, session_id, best_llm

    def stream(
        self,
        prompt_template: Optional[
            Union[
                NDPromptTemplate,
                PromptTemplate,
                NDChatPromptTemplate,
                ChatPromptTemplate,
                str,
            ]
        ] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        input: Optional[Dict[str, Any]] = None,
        metric: NDMetric = NDMetric("accuracy"),
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> Iterator[Union[BaseMessageChunk, BaseModel]]:
        """
        This function calls the NotDiamond backend to fetch the most suitable model for the given prompt,
        and calls the LLM client side to stream the response.

        Parameters:
            prompt_template (Optional(Union[ NDPromptTemplate, PromptTemplate, NDChatPromptTemplate, ChatPromptTemplate, str, ])):
                the prompt template defined by the user. It also supports Langchain prompt template types.
            messages (Optional[List[Dict[str, str]], optional): Can be used instead of prompt_template to pass
                the messages OpenAI style.
            input (Optional[Dict[str, Any]], optional): If the prompt_template contains variables, use input to specify
                                                        the values for those variables. Defaults to None, assuming no variables.
            metric (NDMetric, optional): Metric used by NotDiamond router to choose the best LLM.
                                            Defaults to NDMetric("accuracy").
            response_model (Optional[Type[BaseModel]], optional): If present, will use JsonOutputParser to parse the response into
                                                              the given model. In which case result will a dict.
            **kwargs: Any other arguments that are supported by Langchain's invoke method, will be passed through.

        Raises:
            ApiError: when the NotDiamond API fails

        Yields:
            Iterator[Union[BaseMessageChunk, BaseModel]]: returns the response in chunks.
                If response_model is present, it will return the partial model object
        """

        response_model_parser = None
        if response_model is not None:
            self.verify_against_response_model()
            response_model_parser = JsonOutputParser(
                pydantic_object=response_model
            )

        prompt_template = self._prepare_prompt_template(
            prompt_template=prompt_template,
            messages=messages,
            response_model_parser=response_model_parser,
        )

        if input is None:
            input = {}

        prompt_template.partial_variables = {
            **prompt_template.partial_variables,
            **input,
        }

        best_llm, session_id = model_select(
            prompt_template=prompt_template,
            llm_providers=self.llm_providers,
            metric=metric,
            notdiamond_api_key=self.api_key,
            max_model_depth=self.max_model_depth,
            hash_content=self.hash_content,
            tradeoff=self.tradeoff,
            preference_id=self.preference_id,
            tools=self.tools,
        )

        if not best_llm:
            best_llm = self.default_llm_provider

            if best_llm is None:
                error_message = (
                    "ND couldn't find a suitable model to call."
                    + "To avoid disruptions, we recommend setting a default fallback model or make max depth larger."
                )
                self.call_callbacks("on_api_error", error_message)
                raise ApiError(error_message)
        self.call_callbacks("on_model_select", best_llm, best_llm.model)

        llm = self._llm_from_provider(best_llm, callbacks=self.callbacks)
        if self.tools:
            llm = llm.bind_tools(self.tools)

        if response_model is not None:
            chain = llm | response_model_parser
        else:
            chain = llm

        for chunk in chain.stream(prompt_template.format(), **kwargs):
            if response_model is None:
                yield chunk
            else:
                partial_model = create_partial_model(response_model)
                yield partial_model(**chunk)

    async def astream(
        self,
        prompt_template: Optional[
            Union[
                NDPromptTemplate,
                PromptTemplate,
                NDChatPromptTemplate,
                ChatPromptTemplate,
                str,
            ]
        ] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        input: Optional[Dict[str, Any]] = None,
        metric: NDMetric = NDMetric("accuracy"),
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs,
    ) -> AsyncIterator[Union[BaseMessageChunk, BaseModel]]:
        """
        This function calls the NotDiamond backend to fetch the most suitable model for the given prompt,
        and calls the LLM client side to stream the response. The function is async, so it's suitable for async codebases.

        Parameters:
            prompt_template (Optional(Union[ NDPromptTemplate, PromptTemplate, NDChatPromptTemplate, ChatPromptTemplate, str, ])):
                the prompt template defined by the user. It also supports Langchain prompt template types.
            messages (Optional[List[Dict[str, str]], optional): Can be used instead of prompt_template to pass
                the messages OpenAI style.
            input (Optional[Dict[str, Any]], optional): If the prompt_template contains variables, use input to specify
                                                        the values for those variables. Defaults to None, assuming no variables.
            metric (NDMetric, optional): Metric used by NotDiamond router to choose the best LLM.
                                            Defaults to NDMetric("accuracy").
            response_model (Optional[Type[BaseModel]], optional): If present, will use JsonOutputParser to parse the response into
                                                              the given model. In which case result will a dict.
            **kwargs: Any other arguments that are supported by Langchain's invoke method, will be passed through.

        Raises:
            ApiError: when the NotDiamond API fails

        Yields:
            AsyncIterator[Union[BaseMessageChunk, BaseModel]]: returns the response in chunks.
                If response_model is present, it will return the partial model object
        """

        response_model_parser = None
        if response_model is not None:
            self.verify_against_response_model()
            response_model_parser = JsonOutputParser(
                pydantic_object=response_model
            )

        prompt_template = self._prepare_prompt_template(
            prompt_template=prompt_template,
            messages=messages,
            response_model_parser=response_model_parser,
        )
        best_llm, session_id = await amodel_select(
            prompt_template=prompt_template,
            llm_providers=self.llm_providers,
            metric=metric,
            notdiamond_api_key=self.api_key,
            max_model_depth=self.max_model_depth,
            hash_content=self.hash_content,
            tradeoff=self.tradeoff,
            preference_id=self.preference_id,
            tools=self.tools,
        )

        if input is None:
            input = {}

        prompt_template.partial_variables = {
            **prompt_template.partial_variables,
            **input,
        }

        if not best_llm:
            best_llm = self.default_llm_provider

            if best_llm is None:
                error_message = (
                    "ND couldn't find a suitable model to call."
                    + "To avoid disruptions, we recommend setting a default fallback model or make max depth larger."
                )
                self.call_callbacks("on_api_error", error_message)
                raise ApiError(error_message)
        self.call_callbacks("on_model_select", best_llm, best_llm.model)

        llm = self._llm_from_provider(best_llm, callbacks=self.callbacks)
        if self.tools:
            llm = llm.bind_tools(self.tools)

        if response_model is not None:
            chain = llm | response_model_parser
        else:
            chain = llm

        async for chunk in chain.astream(prompt_template.format(), **kwargs):
            if response_model is None:
                yield chunk
            else:
                partial_model = create_partial_model(response_model)
                yield partial_model(**chunk)

    async def amodel_select(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        prompt_template: Optional[
            Union[
                NDPromptTemplate,
                PromptTemplate,
                NDChatPromptTemplate,
                ChatPromptTemplate,
                str,
            ]
        ] = None,
        input: Optional[Dict[str, Any]] = None,
        model: Optional[List[NDLLMProvider]] = None,
        default: Optional[Union[NDLLMProvider, int, str]] = None,
        max_model_depth: Optional[int] = None,
        latency_tracking: Optional[bool] = None,
        hash_content: Optional[bool] = None,
        tradeoff: Optional[str] = None,
        preference_id: Optional[str] = None,
        metric: NDMetric = NDMetric("accuracy"),
        **kwargs,
    ) -> tuple[str, Optional[NDLLMProvider]]:
        """
        This function calls the NotDiamond backend to fetch the most suitable model for the given prompt,
        and leaves the execution of the LLM call to the developer.
        The function is async, so it's suitable for async codebases.

        Parameters:
            messages (Optional[List[Dict[str, str]], optional): Can be used instead of prompt_template to pass
                the messages OpenAI style.
            prompt_template (Union[ NDPromptTemplate, PromptTemplate, NDChatPromptTemplate, ChatPromptTemplate, str, ]):
                the prompt template defined by the user. It also supports Langchain prompt template types.
            input (Optional[Dict[str, Any]], optional): If the prompt_template contains variables, use input to specify
                                                        the values for those variables. Defaults to None, assuming no variables.
            model (Optional[List[NDLLMProvider]]): List of models to choose from.
            default (Optional[Union[NDLLMProvider, int, str]]): Default LLM provider.
            max_model_depth (Optional[int]): If your top recommended model is down, specify up to which depth
                                                of routing you're willing to go.
            latency_tracking (Optional[bool]): Latency tracking flag.
            hash_content (Optional[bool]): Flag for hashing content before sending to NotDiamond API.
            tradeoff (Optional[str], optional): Define the "cost" or "latency" tradeoff
                                                for the router to determine the best LLM for a given query.
            preference_id (Optional[str]): The ID of the router preference that was configured via the Dashboard.
                                            Defaults to None.
            metric (NDMetric, optional): Metric used by NotDiamond router to choose the best LLM.
                                            Defaults to NDMetric("accuracy").
            **kwargs: Any other arguments that are supported by Langchain's invoke method, will be passed through.

        Returns:
            tuple[str, Optional[NDLLMProvider]]: returns the session_id and the chosen LLM provider
        """
        prompt_template = self._prepare_prompt_template(
            prompt_template,
            messages,
        )

        if input is None:
            input = {}

        prompt_template.partial_variables = {
            **prompt_template.partial_variables,
            **input,
        }

        if model is not None:
            llm_providers = self._parse_llm_providers_data(model)
            self.llm_providers = llm_providers

        self.validate_params(
            default=default,
            max_model_depth=max_model_depth,
            latency_tracking=latency_tracking,
            hash_content=hash_content,
            tradeoff=tradeoff,
            preference_id=preference_id,
        )

        best_llm, session_id = await amodel_select(
            prompt_template=prompt_template,
            llm_providers=self.llm_providers,
            metric=metric,
            notdiamond_api_key=self.api_key,
            max_model_depth=self.max_model_depth,
            hash_content=self.hash_content,
            tradeoff=self.tradeoff,
            preference_id=self.preference_id,
            tools=self.tools,
        )

        if not best_llm and self.default is not None:
            print("ND API error. Falling back to default provider.")
            best_llm = self.default_llm_provider
        self.call_callbacks("on_model_select", best_llm, best_llm.model)

        return session_id, best_llm

    def model_select(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        prompt_template: Optional[
            Union[
                NDPromptTemplate,
                PromptTemplate,
                NDChatPromptTemplate,
                ChatPromptTemplate,
                str,
            ]
        ] = None,
        input: Optional[Dict[str, Any]] = None,
        model: Optional[List[NDLLMProvider]] = None,
        default: Optional[Union[NDLLMProvider, int, str]] = None,
        max_model_depth: Optional[int] = None,
        latency_tracking: Optional[bool] = None,
        hash_content: Optional[bool] = None,
        tradeoff: Optional[str] = None,
        preference_id: Optional[str] = None,
        metric: NDMetric = NDMetric("accuracy"),
        **kwargs,
    ) -> tuple[str, Optional[NDLLMProvider]]:
        """
        This function calls the NotDiamond backend to fetch the most suitable model for the given prompt,
        and leaves the execution of the LLM call to the developer.

        Parameters:
            messages (Optional[List[Dict[str, str]], optional): Can be used instead of prompt_template to pass
                the messages OpenAI style.
            prompt_template (Union[ NDPromptTemplate, PromptTemplate, NDChatPromptTemplate, ChatPromptTemplate, str, ]):
                the prompt template defined by the user. It also supports Langchain prompt template types.
            input (Optional[Dict[str, Any]], optional): If the prompt_template contains variables, use input to specify
                                                        the values for those variables. Defaults to None, assuming no variables.
            model (Optional[List[NDLLMProvider]]): List of models to choose from.
            default (Optional[Union[NDLLMProvider, int, str]]): Default LLM provider.
            max_model_depth (Optional[int]): If your top recommended model is down, specify up to which depth
                                                of routing you're willing to go.
            latency_tracking (Optional[bool]): Latency tracking flag.
            hash_content (Optional[bool]): Flag for hashing content before sending to NotDiamond API.
            tradeoff (Optional[str], optional): Define the "cost" or "latency" tradeoff
                                                for the router to determine the best LLM for a given query.
            preference_id (Optional[str]): The ID of the router preference that was configured via the Dashboard.
                                            Defaults to None.
            metric (NDMetric, optional): Metric used by NotDiamond router to choose the best LLM.
                                            Defaults to NDMetric("accuracy").
            **kwargs: Any other arguments that are supported by Langchain's invoke method, will be passed through.

        Returns:
            tuple[str, Optional[NDLLMProvider]]: returns the session_id and the chosen LLM provider
        """
        prompt_template = self._prepare_prompt_template(
            prompt_template,
            messages,
        )

        if input is None:
            input = {}

        prompt_template.partial_variables = {
            **prompt_template.partial_variables,
            **input,
        }

        if model is not None:
            llm_providers = self._parse_llm_providers_data(model)
            self.llm_providers = llm_providers

        self.validate_params(
            default=default,
            max_model_depth=max_model_depth,
            latency_tracking=latency_tracking,
            hash_content=hash_content,
            tradeoff=tradeoff,
            preference_id=preference_id,
        )

        best_llm, session_id = model_select(
            prompt_template=prompt_template,
            llm_providers=self.llm_providers,
            metric=metric,
            notdiamond_api_key=self.api_key,
            max_model_depth=self.max_model_depth,
            hash_content=self.hash_content,
            tradeoff=self.tradeoff,
            preference_id=self.preference_id,
            tools=self.tools,
        )

        if not best_llm and self.default is not None:
            print("ND API error. Falling back to default provider.")
            best_llm = self.default_llm_provider
        self.call_callbacks("on_model_select", best_llm, best_llm.model)

        return session_id, best_llm

    async def _async_invoke_with_latency_tracking(
        self,
        session_id: str,
        chain: Any,
        llm_provider: NDLLMProvider,
        input: Optional[Dict[str, Any]] = {},
        is_default: bool = True,
        **kwargs,
    ):
        if session_id in ("NO-SESSION-ID", "") and not is_default:
            error_message = (
                "ND session_id is not valid for latency tracking."
                + "Please check the API response."
            )
            self.call_callbacks("on_api_error", error_message)
            raise ApiError(error_message)

        start_time = time.time()

        result = await chain.ainvoke(input, **kwargs)

        end_time = time.time()

        if isinstance(result, str):
            result = AIMessage(content=result)

        tokens_completed = token_counter(
            model=llm_provider.model,
            messages=[{"role": "assistant", "content": result.content}],
        )
        tokens_per_second = tokens_completed / (end_time - start_time)

        report_latency(
            session_id=session_id,
            llm_provider=llm_provider,
            tokens_per_second=tokens_per_second,
            notdiamond_api_key=self.api_key,
        )
        self.call_callbacks(
            "on_latency_tracking", session_id, llm_provider, tokens_per_second
        )

        return result

    def _invoke_with_latency_tracking(
        self,
        session_id: str,
        chain: Any,
        llm_provider: NDLLMProvider,
        input: Optional[Dict[str, Any]] = {},
        is_default: bool = True,
        **kwargs,
    ):
        if session_id in ("NO-SESSION-ID", "") and not is_default:
            error_message = (
                "ND session_id is not valid for latency tracking."
                + "Please check the API response."
            )
            self.call_callbacks("on_api_error", error_message)
            raise ApiError(error_message)

        start_time = time.time()
        result = chain.invoke(input, **kwargs)
        end_time = time.time()

        if isinstance(result, str):
            result = AIMessage(content=result)

        tokens_completed = token_counter(
            model=llm_provider.model,
            messages=[{"role": "assistant", "content": result.content}],
        )
        tokens_per_second = tokens_completed / (end_time - start_time)

        report_latency(
            session_id=session_id,
            llm_provider=llm_provider,
            tokens_per_second=tokens_per_second,
            notdiamond_api_key=self.api_key,
        )
        self.call_callbacks(
            "on_latency_tracking", session_id, llm_provider, tokens_per_second
        )

        return result

    @staticmethod
    def _llm_from_provider(
        provider: NDLLMProvider,
        callbacks: Optional[
            List[Union[BaseCallbackHandler, NDLLMBaseCallbackHandler]]
        ],
    ) -> Any:
        default_kwargs = {"max_retries": 5, "timeout": 120}
        passed_kwargs = {**default_kwargs, **provider.kwargs}

        if provider.provider == "openai":
            return ChatOpenAI(
                openai_api_key=provider.api_key,
                model_name=provider.model,
                callbacks=callbacks,
                **passed_kwargs,
            )
        if provider.provider == "anthropic":
            return ChatAnthropic(
                anthropic_api_key=provider.api_key,
                model=provider.model,
                callbacks=callbacks,
                **passed_kwargs,
            )
        if provider.provider == "google":
            return ChatGoogleGenerativeAI(
                google_api_key=provider.api_key,
                model=provider.model,
                convert_system_message_to_human=True,
                callbacks=callbacks,
                **passed_kwargs,
            )
        if provider.provider == "cohere":
            return ChatCohere(
                cohere_api_key=provider.api_key,
                model=provider.model,
                callbacks=callbacks,
                **passed_kwargs,
            )
        if provider.provider == "mistral":
            return ChatMistralAI(
                mistral_api_key=provider.api_key,
                model=provider.model,
                callbacks=callbacks,
                **passed_kwargs,
            )
        if provider.provider == "togetherai":
            provider_settings = settings.PROVIDERS.get(provider.provider, None)
            model_prefixes = provider_settings.get("model_prefix", None)
            model_prefix = model_prefixes.get(provider.model, None)
            del passed_kwargs["max_retries"]
            del passed_kwargs["timeout"]

            model = provider.model
            if model_prefix is not None:
                model = f"{model_prefix}/{provider.model}"
            print(f"MODEL: {model}")
            return Together(
                together_api_key=provider.api_key,
                model=model,
                callbacks=callbacks,
                **passed_kwargs,
            )
        if provider.provider == "perplexity":
            del passed_kwargs["max_retries"]
            passed_kwargs["request_timeout"] = passed_kwargs["timeout"]
            del passed_kwargs["timeout"]
            return ChatPerplexity(
                pplx_api_key=provider.api_key,
                model=provider.model,
                callbacks=callbacks,
                **passed_kwargs,
            )
        raise ValueError(f"Unsupported provider: {provider.provider}")

    @staticmethod
    def _prepare_prompt_template(
        prompt_template, messages=None, response_model_parser=None
    ) -> Union[NDPromptTemplate, NDChatPromptTemplate]:
        resulting_prompt_template = None
        if prompt_template is not None and messages is not None:
            print(
                "Warning: prompt_template value is overriding messages value. Set one of those values for optimal performance."
            )
        if prompt_template is not None:
            if isinstance(prompt_template, NDPromptTemplate) or isinstance(
                prompt_template, NDChatPromptTemplate
            ):
                resulting_prompt_template = prompt_template
            elif isinstance(prompt_template, str):
                resulting_prompt_template = NDPromptTemplate(
                    template=prompt_template
                )
            elif isinstance(prompt_template, StringPromptValue):
                resulting_prompt_template = NDChatPromptTemplate.from_messages(
                    prompt_template.to_messages()
                )
            elif isinstance(prompt_template, PromptTemplate):
                resulting_prompt_template = (
                    NDPromptTemplate.from_langchain_prompt_template(
                        prompt_template
                    )
                )
            elif isinstance(prompt_template, ChatPromptTemplate):
                resulting_prompt_template = (
                    NDChatPromptTemplate.from_langchain_chat_prompt_template(
                        prompt_template
                    )
                )
            elif isinstance(prompt_template, list):
                if all(isinstance(pt, BaseMessage) for pt in prompt_template):
                    resulting_prompt_template = (
                        NDChatPromptTemplate.from_messages(prompt_template)
                    )
            if resulting_prompt_template is None:
                raise ValueError(
                    f"Unsupported prompt_template type {type(prompt_template)}"
                )
        if messages is not None:
            resulting_prompt_template = (
                NDChatPromptTemplate.from_openai_messages(messages)
            )

        if resulting_prompt_template is None:
            raise ValueError("prompt_template or messages must be specified.")

        if response_model_parser is not None:
            resulting_prompt_template = (
                resulting_prompt_template.inject_model_instruction(
                    response_model_parser
                )
            )

        return resulting_prompt_template

    def bind_tools(
        self,
        tools: Sequence[Union[Dict[str, Any], Callable]],
    ) -> "NDLLM":
        """
        Bind tools to the LLM object. The tools will be passed to the LLM object when invoking it.
        Results in the tools being available in the LLM object.
        You can access the tool_calls in the result via `result.tool_calls`.
        """

        for provider in self.llm_providers:
            if provider.model not in settings.PROVIDERS[provider.provider].get(
                "support_tools", []
            ):
                raise ApiError(
                    f"{provider.provider}/{provider.model} does not support function calling."
                )
        self.tools = tools

        return self

    def call_callbacks(self, function_name: str, *args, **kwargs) -> None:
        """
        Call all callbacks with a specific function name.
        """

        if self.callbacks is None:
            return

        for callback in self.callbacks:
            if hasattr(callback, function_name):
                getattr(callback, function_name)(*args, **kwargs)

    def verify_against_response_model(self) -> bool:
        """
        Verify that the LLM providers support response modeling.
        """

        for provider in self.llm_providers:
            if provider.model not in settings.PROVIDERS[provider.provider].get(
                "support_response_model", []
            ):
                raise ApiError(
                    f"{provider.provider}/{provider.model} does not support response modeling."
                )

        return True

    def validate_params(
        self,
        default: Optional[Union[NDLLMProvider, int, str]] = None,
        max_model_depth: Optional[int] = None,
        latency_tracking: Optional[bool] = None,
        hash_content: Optional[bool] = None,
        tradeoff: Optional[str] = None,
        preference_id: Optional[str] = None,
    ):
        if default is not None:
            self.default = default

        if max_model_depth is not None:
            self.max_model_depth = max_model_depth

        if self.llm_providers is None or len(self.llm_providers) == 0:
            raise MissingLLMProviders(
                "No LLM provider speficied. Specify at least one."
            )

        if self.max_model_depth is None:
            self.max_model_depth = len(self.llm_providers)

        if self.max_model_depth == 0:
            raise ValueError("max_model_depth has to be bigger than 0.")

        if self.max_model_depth > len(self.llm_providers):
            print(
                "WARNING: max_model_depth cannot be bigger than the number of LLM providers."
            )
            self.max_model_depth = len(self.llm_providers)

        if tradeoff is not None:
            if tradeoff not in ["cost", "latency"]:
                raise ValueError(
                    "Invalid tradeoff. Accepted values: cost, latency."
                )
            self.tradeoff = tradeoff

        if preference_id is not None:
            self.preference_id = preference_id

        if latency_tracking is not None:
            self.latency_tracking = latency_tracking

        if hash_content is not None:
            self.hash_content = hash_content
