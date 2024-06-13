from typing import Any, Awaitable, Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from observe.logger import get_logger

from llm.common import InternalPredictionError, PredictionError

logger = get_logger()


async def retry_convo(
    model: BaseChatModel,
    model_config: RunnableConfig,
    prompt: ChatPromptTemplate,
    prompt_params: dict[str, Any],
    format_response_fn: Callable[[str], Awaitable[Any]],
    validate_response_fn: Callable[[Any], Awaitable[bool]],
    retry: int = 4,
    label: str = None,
) -> Any:
    logger.info("Starting retry convo loop", label=label)
    iteration = 0
    while iteration < retry:
        # ask question
        logger.info("Asking question", label=label)
        chain = prompt | model
        res_ans = await chain.ainvoke(prompt_params, model_config)
        ans = await format_response_fn(res_ans.content)

        # validate if the answer is correct
        try:
            if await validate_response_fn(ans):
                return ans
            logger.error(
                "Answer is not correct. Asking question again", label=label, ans=ans
            )
        except InternalPredictionError as e:
            logger.error(
                "Answer is not correct. Asking question again",
                label=label,
                ans=ans,
                error=str(e),
            )

        iteration += 1

    raise PredictionError("reached max retry limit")
