from typing import Any


from danswer.chat.chat_utils import combine_message_chain
from danswer.configs.model_configs import GEN_AI_HISTORY_CUTOFF
from danswer.llm.answering.models import PreviousMessage
from danswer.llm.interfaces import LLM
from danswer.llm.utils import message_to_string
from danswer.prompts.constants import GENERAL_SEP_PAT
from danswer.tools.tool import Tool

from danswer.utils.logger import setup_logger

logger = setup_logger()


SINGLE_TOOL_SELECTION_PROMPT = f"""
You are an expert at selecting the most useful tool to run for answering the query.
You will be given a numbered list of tools and their arguments, a message history, and a query.
You will select a single tool that will be most useful for answering the query, and provide only the number corresponding to the tool you want to use.

Conversation History:
{GENERAL_SEP_PAT}
{{chat_history}}
{GENERAL_SEP_PAT}

Query:
{{query}}

Tools:
{{tool_list}}

Respond with EXACTLY and ONLY the number corresponding to the tool you want to use.

Your selection:
"""

def select_single_tool_for_non_tool_calling_llm(
    tools_and_args: list[tuple[Tool, dict[str, Any]]],
    history: list[PreviousMessage],
    query: str,
    llm: LLM,
) -> tuple[Tool, dict[str, Any]] | None:
    if len(tools_and_args) == 1:
        return tools_and_args[0]

    tool_list_str = "\n".join(
        f"""{ind}: {tool.name()} ({args}) - {tool.description()}"""
        for ind, (tool, args) in enumerate(tools_and_args)
    )

    history_str = combine_message_chain(
        messages=history,
        token_limit=GEN_AI_HISTORY_CUTOFF,
    )
    prompt = SINGLE_TOOL_SELECTION_PROMPT.format(
        tool_list=tool_list_str, chat_history=history_str, query=query
    )
    output = message_to_string(llm.invoke(prompt))
    try:
        tool_ind = int(output)
        return tools_and_args[tool_ind]
    except Exception:
        logger.error(f"Failed to select single tool for non-tool-calling LLM: {output}")
        return None