from typing import Any, Awaitable, Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from observe.logger import get_logger

from llm.common import PredictionError

logger = get_logger()


def ask_again_convo(
    model: BaseChatModel,
    model_config: RunnableConfig,
    prompt: ChatPromptTemplate,
    prompt_params: dict[str, Any],
    prompt_ask_again_message: HumanMessage,
    format_response_fn: Callable[[str], Any],
    validate_response_fn: Callable[[Any], bool],
    retry: int = 4,
    label: str = None,
) -> Any:
    # ask question the first time
    logger.info("Asking question the first time", label=label)
    chain = prompt | model
    res_ans_first = chain.invoke(prompt_params, model_config)
    ans_first = format_response_fn(res_ans_first.content)

    # validate if the answer is correct
    if validate_response_fn(ans_first):
        return ans_first
    logger.info(
        "Answer is not correct. Asking question again", label=label, ans_first=ans_first
    )

    # start asking question again loop
    iteration = 0
    prompt_ask_again = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            prompt_ask_again_message,  # first ask again message
        ]
    )
    chat_ask_again_history = []
    while iteration < retry:
        chat_history = (
            prompt.format_messages(**prompt_params)
            + [res_ans_first]
            + chat_ask_again_history
        )
        prompt_ask_again_params = {"chat_history": chat_history}
        chain_ask_again = prompt_ask_again | model
        # ask question again
        res_ans_again = chain_ask_again.invoke(prompt_ask_again_params, model_config)
        ans_again = format_response_fn(res_ans_again.content)
        if validate_response_fn(ans_again):
            return ans_again

        iteration += 1
        chat_ask_again_history.extend([prompt_ask_again_message, res_ans_again])
        logger.info(
            "Answer is not correct. Asking question again",
            label=label,
            retry=iteration,
            ans_again=ans_again,
        )

    raise PredictionError("Unable to predict a valid answer")


async def async_ask_again_convo(
    model: BaseChatModel,
    model_config: RunnableConfig,
    prompt: ChatPromptTemplate,
    prompt_params: dict[str, Any],
    prompt_ask_again_message: HumanMessage,
    format_response_fn: Callable[[str], Awaitable[Any]],
    validate_response_fn: Callable[[Any], Awaitable[bool]],
    retry: int = 4,
    label: str = None,
) -> Any:
    # ask question the first time
    logger.info("Asking question the first time", label=label)
    chain = prompt | model
    res_ans_first = await chain.ainvoke(prompt_params, model_config)
    ans_first = await format_response_fn(res_ans_first.content)

    # validate if the answer is correct
    if await validate_response_fn(ans_first):
        return ans_first
    logger.info(
        "Answer is not correct. Asking question again", label=label, ans_first=ans_first
    )

    # start asking question again loop
    iteration = 0
    prompt_ask_again = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            prompt_ask_again_message,  # first ask again message
        ]
    )
    chat_ask_again_history = []
    while iteration < retry:
        chat_history = (
            prompt.format_messages(**prompt_params)
            + [res_ans_first]
            + chat_ask_again_history
        )
        prompt_ask_again_params = {"chat_history": chat_history}
        chain_ask_again = prompt_ask_again | model
        # ask question again
        res_ans_again = await chain_ask_again.ainvoke(
            prompt_ask_again_params, model_config
        )
        ans_again = await format_response_fn(res_ans_again.content)
        if await validate_response_fn(ans_again):
            return ans_again

        iteration += 1
        chat_ask_again_history.extend([prompt_ask_again_message, res_ans_again])
        logger.info(
            "Answer is not correct. Asking question again",
            label=label,
            retry=iteration,
            ans_again=ans_again,
        )

    raise PredictionError("Unable to predict a valid answer")
