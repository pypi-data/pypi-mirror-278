from typing import Any, Dict, List, Optional, Union

from langchain.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.string import get_template_variables


class NDPromptTemplate(PromptTemplate):
    """Custom implementation of NDPromptTemplate
    Starting reference is from here:
    https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.prompt.PromptTemplate.html
    """

    def __init__(
        self,
        template: str,
        input_variables: Optional[List[str]] = None,
        partial_variables: Optional[Dict[str, Any]] = {},
    ):
        if input_variables is None:
            input_variables = get_template_variables(template, "f-string")

        if partial_variables:
            input_variables = []

        super(NDPromptTemplate, self).__init__(
            template=template,
            input_variables=input_variables,
            partial_variables=partial_variables,
        )

    @classmethod
    def from_langchain_prompt_template(cls, prompt_template: PromptTemplate):
        return cls(
            template=prompt_template.template,
            input_variables=prompt_template.input_variables,
            partial_variables=prompt_template.partial_variables,
        )

    def format(self, **kwargs: Any) -> str:
        """Format the prompt template with the given variables and convert it to NDPromptTemplate."""
        return super(NDPromptTemplate, self).format(**kwargs)

    def optimize(self):
        print("Not yet implemented!")

    def prepare_for_request(self):
        return [{"role": "user", "content": self.format()}]

    def inject_model_instruction(self, parser: JsonOutputParser):
        format_instructions = parser.get_format_instructions()
        format_instructions = format_instructions.replace("{", "{{").replace(
            "}", "}}"
        )
        self.template = format_instructions + "\n" + self.template

        return self


class NDChatPromptTemplate(ChatPromptTemplate):
    """
    Starting reference is from
    here:https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html
    """

    def __init__(
        self,
        messages: Optional[List] = None,
        input_variables: Optional[List[str]] = None,
        partial_variables: [str, Any] = dict,
    ):
        if messages is None:
            messages = []
        if partial_variables:
            input_variables = []

        super().__init__(
            messages=messages,
            input_variables=input_variables,
            partial_variables=partial_variables,
        )

    @property
    def template(self):
        message = """
        SYSTEM: {system_prompt}
        CONTEXT: {context_prompt}
        QUERY: {user_query}
        """
        return message

    @classmethod
    def from_langchain_chat_prompt_template(
        cls, chat_prompt_template: ChatPromptTemplate
    ):
        return cls(
            messages=chat_prompt_template.messages,
            input_variables=chat_prompt_template.input_variables,
            partial_variables=chat_prompt_template.partial_variables,
        )

    @classmethod
    def from_openai_messages(cls, messages: List[Dict[str, str]]):
        transformed_messages = []
        for message in messages:
            if message["role"] == "system":
                transformed_messages.append(SystemMessage(message["content"]))
            elif message["role"] == "assistant":
                transformed_messages.append(AIMessage(message["content"]))
            elif message["role"] == "user":
                transformed_messages.append(HumanMessage(message["content"]))
            else:
                raise ValueError(f"Unsupported role: {message['role']}")
        return cls(
            messages=transformed_messages,
            input_variables=None,
            partial_variables={},
        )

    def format(self, **kwargs: Any) -> str:
        """Format the prompt template with the given variables. and converts it to NDChatPromptTemplate."""
        return super(NDChatPromptTemplate, self).format(**kwargs)

    def get_last_human_message(self, formated_messages: List) -> str:
        for message in reversed(formated_messages):
            if isinstance(message, HumanMessage):
                return message.content

        raise ValueError("No human message found in the list of messages.")

    def get_role_of_message(
        self, message: Union[AIMessage, HumanMessage, SystemMessage]
    ) -> str:
        if isinstance(message, SystemMessage):
            return "system"
        if isinstance(message, AIMessage):
            return "assistant"
        if isinstance(message, HumanMessage):
            return "user"
        raise ValueError(f"Unsupported message type: {type(message)}")

    def prepare_for_request(self):
        formated_messages = self.format_messages(**self.partial_variables)
        messages = []

        for message in formated_messages:
            if (
                isinstance(message, SystemMessage)
                or isinstance(message, AIMessage)
                or isinstance(message, HumanMessage)
            ):
                messages.append(
                    {
                        "role": self.get_role_of_message(message),
                        "content": message.content,
                    }
                )

        return messages

    def inject_model_instruction(self, parser: JsonOutputParser):
        format_instructions = parser.get_format_instructions()
        format_instructions = format_instructions.replace("{", "{{").replace(
            "}", "}}"
        )
        self.messages[0].content = (
            format_instructions + "\n" + self.messages[0].content
        )

        return self
