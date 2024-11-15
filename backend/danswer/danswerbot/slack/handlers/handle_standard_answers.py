from slack_sdk import WebClient
from sqlalchemy.orm import Session

from danswer.danswerbot.slack.models import SlackMessageInfo
from danswer.db.models import Prompt
from danswer.db.models import SlackBotConfig
from danswer.utils.logger import DanswerLoggingAdapter
from danswer.utils.logger import setup_logger
from danswer.utils.variable_functionality import fetch_versioned_implementation

logger = setup_logger()


def handle_standard_answers(
    message_info: SlackMessageInfo,
    receiver_ids: list[str] | None,
    slack_bot_config: SlackBotConfig | None,
    prompt: Prompt | None,
    logger: DanswerLoggingAdapter,
    client: WebClient,
    db_session: Session,
) -> bool:
    """Returns whether one or more Standard Answer message blocks were
    emitted by the Slack bot"""
    versioned_handle_standard_answers = fetch_versioned_implementation(
        "danswer.danswerbot.slack.handlers.handle_standard_answers",
        "_handle_standard_answers",
    )
    return versioned_handle_standard_answers(
        message_info=message_info,
        receiver_ids=receiver_ids,
        slack_bot_config=slack_bot_config,
        prompt=prompt,
        logger=logger,
        client=client,
        db_session=db_session,
    )


def _handle_standard_answers(
    message_info: SlackMessageInfo,
    receiver_ids: list[str] | None,
    slack_bot_config: SlackBotConfig | None,
    prompt: Prompt | None,
    logger: DanswerLoggingAdapter,
    client: WebClient,
    db_session: Session,
) -> bool:
    """
    Standard Answers are a paid Enterprise Edition feature. This is the fallback
    function handling the case where EE features are not enabled.

    Always returns false i.e. since EE features are not enabled, we NEVER create any
    Slack message blocks.
    """
    return False
