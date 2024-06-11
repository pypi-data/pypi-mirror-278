"""Hermes templating engine for structured prefix generation."""

# TODO: import ansible core filters.
# TODO: Move this out of the hermes wheel and back into the tokenizer core.

import re
from logging import LoggerAdapter
from typing import Union

from constants import DEFAULT_USERNAME, NARRATOR_NAME
from context import Context
from contrib.lm_prefix_utils import get_character_priming
from decorators import monitor
from exceptions import MissingContextData
from structured_prefix import StructuredPrefix
from template import TemplatingEngine


# TODO: use ansible core filters instead of custom filters.
# BEGIN: Hermes Filters
# TODO: necessary for correct YAML parsing. Figure out a better solution.
# Tried using folded block scalar ">" but it didn't work.
def escape_sequences(message: str) -> str:
    """Escape sequences that will break yaml parsing."""
    return message.replace(Context.NEWLINE, Context.ESCAPED_NEWLINE).replace(
        Context.CARRIAGE_RETURN, Context.ESCAPED_CARRIAGE_RETURN
    )


def maybe_inject_narrator(message: str, default_author: str = NARRATOR_NAME) -> str:
    """Inject narrator into the message if applicable."""
    if re.match(r"^[\w-]+:", message):
        return message
    return f"{default_author}: {message}"


def raise_missing_context_data(key: str):
    """Raise missing data from jinja context."""
    raise MissingContextData(f"Missing required key in jinja context: {key=}")


def canonicalize_user_name(name: Union[str, None]) -> str:
    """Makes name format consistent with author names we use in training data."""
    # The "-" is used in upstream components and should be overriden to default value.
    if name is None or not name or name == "-":
        return DEFAULT_USERNAME
    return "-".join(name.split())


# END: Hermes Filters


@monitor
def build_structured_prefix(
    contextual_logger: LoggerAdapter,
    structured_prefix: StructuredPrefix,
    close_last_message: bool = False,
    truncation_step: int = None,
) -> dict:
    """Build structured prefix using Hermes templating engine."""
    del close_last_message  # TODO: support long streaming.

    # TODO: move templating engine into Context class.
    engine = TemplatingEngine(logger=contextual_logger)
    jinja_context = _build_jinja_context(
        structured_prefix=structured_prefix,
        contextual_logger=contextual_logger,
    )

    rendered_template = engine.render_template(
        jinja_context,
        template_name=structured_prefix.hermes_generation_template_name,
        raw_template=structured_prefix.hermes_generation_template,
    )

    # TODO: add prometheus logging for latency.
    lm_context = Context(
        contextual_logger=contextual_logger,
        rendered_template=rendered_template,
        structured_prefix=structured_prefix,
        truncation_step=truncation_step,
    )
    lm_context.load_yaml()
    lm_context.tokenize()
    lm_context.truncate()
    lm_context.validate()

    return {
        "character_definitions": structured_prefix.character_definitions,
        "chat_history": structured_prefix.chat_history[
            -lm_context.num_messages_included :
        ],
        "chat_hist_global_index": 0,
        "reply_prompt": lm_context.raw_reply_prompt,
        "space_added": True,
        "token_limit": structured_prefix.token_limit,
        "tokenized_context": lm_context.tokenized_context,
        "timestamp": lm_context.timestamp_str,
        "lm_context": lm_context,
    }


@monitor
def _build_jinja_context(
    structured_prefix: StructuredPrefix,
    contextual_logger: LoggerAdapter,
) -> dict:
    if structured_prefix.raw_prompt_data_dict is None:
        structured_prefix.parse_raw_prompt_data(contextual_logger=contextual_logger)
    if structured_prefix.chat_context_messages is None:
        structured_prefix.parse_chat_context_messages(
            contextual_logger=contextual_logger
        )

    # TODO: handle this in the template not in logical layer.
    username = structured_prefix.raw_prompt_data_dict.get("username", "")
    if not username or username == "-":
        username = DEFAULT_USERNAME

    return {
        ### Raw prompt data that has not been tampered with ###
        "chat_type": structured_prefix.raw_prompt_data_dict.get("chat_type", ""),
        "character": structured_prefix.raw_prompt_data_dict.get("character", {}),
        "user_country_code": structured_prefix.raw_prompt_data_dict.get(
            "user_country_code", ""
        ),
        "username": username,
        "persona_definition": structured_prefix.raw_prompt_data_dict.get(
            "persona_definition", ""
        ),
        "is_proactive": structured_prefix.raw_prompt_data_dict.get(
            "is_proactive", False
        ),
        "proactive_metadata": structured_prefix.raw_prompt_data_dict.get(
            "proactive_metadata", {}
        ),
        "chat_context_messages": structured_prefix.chat_context_messages,
        ###  Constants data ###
        "narrator_name": NARRATOR_NAME,
        ### Legacy prompt data that has been tampered with by upstream components ###
        "character_definition_messages": structured_prefix.character_definitions,
        "pinned_history": structured_prefix.pinned_history or [],
        "chat_history": structured_prefix.chat_history,
        "reply_prompt": structured_prefix.reply_prompt,
        "timestamp": structured_prefix.timestamp,
        ### Filters ###
        # TODO: import ansible core filters instead of custom filters.
        "maybe_inject_narrator": maybe_inject_narrator,
        "escape_sequences": escape_sequences,
        "get_character_priming": get_character_priming,
        "canonicalize_user_name": canonicalize_user_name,
        "raise_missing_context_data": raise_missing_context_data,
    }
