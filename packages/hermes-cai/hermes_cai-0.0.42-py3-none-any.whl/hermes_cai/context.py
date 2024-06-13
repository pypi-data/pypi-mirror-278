"""Context module for Hermes CAI."""

import math
import re
from dataclasses import dataclass
from functools import reduce
from logging import LoggerAdapter

import yaml
from constants import VALID_PROMPT_STRING_PATTERNS
from contrib.lm_prefix_utils import TokenizedContext, get_tokenizer
from decorators import monitor
from exceptions import (
    InvalidPromptError,
    MessageStartIdxNotFound,
    TimestampIdxNotFoundError,
    TimestampStrNotFoundError,
    TokenLimitExceededError,
)
from metrics import Metrics
from structured_prefix import StructuredPrefix
from yaml import CSafeLoader


@dataclass
class PromptPart:
    """Container representing repeated prompt parts from the template."""

    name: str
    raw_string: str
    tokens: list[int] = None


class Context:
    """Context holds all essential data and business logic for constructing prompts."""

    BOD_PART_NAME: str = "bod_ts"
    REPLY_PROMPT_PART_NAME: str = "reply_prompt"
    CACHE_FRIENDLY_TRUNCATION_STEP: int = 1000
    BOD: str = "<|beginningofdialog|>"
    BOM: str = "<|beginningofmessage|>"
    SPACE_MARKER: str = "<|space|>"
    CARRIAGE_RETURN: str = "\r"
    ESCAPED_CARRIAGE_RETURN: str = "\\r"
    NEWLINE: str = "\n"
    ESCAPED_NEWLINE: str = "\\n"
    SINGLE_QUOTE: str = "'"
    ESCAPED_SINGLE_QUOTE: str = "'"

    @monitor
    def __init__(
        self,
        contextual_logger: LoggerAdapter,
        rendered_template: str,
        structured_prefix: StructuredPrefix,
        truncation_step: int = None,
    ):
        """Initialize context."""
        if truncation_step is not None and truncation_step <= 0:
            raise ValueError(f"Invalid truncation step: {truncation_step=}")

        self._logger = contextual_logger
        self.prompt_parts = None
        # Special case for reconstructing full prompts that have been truncated.
        self.prompt_parts_bak = None
        self.rendered_template = rendered_template
        self.token_limit = structured_prefix.token_limit
        self.tokenizer = get_tokenizer()
        self.idx_after_timestamp = -1
        self.timestamp_str = None
        self.num_total_pinned_message_tokens = 0
        self.num_total_tokens = 0
        self.num_tokens_truncated = 0
        self.message_start_idx = -1
        self.num_messages_included = 0
        self.num_messages_truncated = 0
        self.num_total_pinned_messages = 0
        self.num_total_messages = 0
        self.raw_reply_prompt = ""
        self.truncation_step = truncation_step

    @monitor
    def load_yaml(self):
        """Load yaml from rendered template."""
        self.prompt_parts = self._load_yaml(self.rendered_template)

    @monitor
    def validate(self):
        """Raises if the current Context object is invalid by certain heuristics."""
        # Cache prompt tokens and prompt string as it can be expensive to compute.
        prompt_tokens = self.prompt_tokens
        prompt_string = self.prompt_string

        if len(self.prompt_parts) > 1 and self.prompt_parts[1].raw_string.startswith(
            Context.BOM
        ):
            raise InvalidPromptError(
                f"First message should NOT contain {Context.BOM=}: {self.prompt_parts[1]=}"
            )

        for pattern in VALID_PROMPT_STRING_PATTERNS:
            if not re.match(pattern, prompt_string):
                raise InvalidPromptError(
                    f"Invalid prompt regex: {pattern=} {str(prompt_string)=}"
                )

        if len(prompt_tokens) > self.token_limit:
            raise TokenLimitExceededError(
                f"Token limit exceeded: {len(prompt_tokens)=} {self.token_limit=}"
            )

        if not self.timestamp_str:
            raise TimestampStrNotFoundError(
                f"Timestamp string not found: {self.timestamp_str=}"
            )

        if self.idx_after_timestamp == -1:
            raise TimestampIdxNotFoundError(
                f"Timestamp index not found: {self.idx_after_timestamp=}"
            )

    @monitor
    def tokenize(self):
        """Cleans, tokenizes and maybe extracts some metadata of each prompt part."""
        # Tokenize each prompt part.
        for idx, part in enumerate(self.prompt_parts):
            self._clean_raw_string(part)
            self._tokenize_part(part)
            self._maybe_extract_metadata_and_clean(idx=idx, prompt_part=part)

    @monitor
    def truncate(self):
        """Truncate messages if the token limit is exceeded."""
        if self.message_start_idx == -1:
            raise MessageStartIdxNotFound(
                f"Message start index not found: {self.message_start_idx=}"
            )

        num_tokens_to_truncate = self._calculate_num_tokens_to_truncate()
        i = self.message_start_idx
        if num_tokens_to_truncate:
            self._logger.info(
                f"Truncating... {num_tokens_to_truncate=}; {self.num_total_tokens=}; {self.num_total_messages=}"
            )
        while (
            self.num_tokens_truncated < num_tokens_to_truncate
            and i < self.message_start_idx + self.num_total_messages
        ):
            part = self.prompt_parts[i]
            self.num_tokens_truncated += len(part.tokens)
            self.num_messages_truncated += 1
            i += 1

        self.num_messages_included = (
            self.num_total_messages - self.num_messages_truncated
        )
        self._truncate()

        # A short-term hack to fix the special case of first message should not have bom.
        # TODO: Rethink this in the future to see if we can take it out of the logical layer.
        if (
            len(self.prompt_parts) > 1
            and Context.BOM in self.prompt_parts[1].raw_string
        ):
            self.prompt_parts[1].raw_string = self.prompt_parts[1].raw_string.replace(
                Context.BOM, " "
            )
            self._tokenize_part(self.prompt_parts[1])

    @property
    def tokenized_context(self) -> TokenizedContext:
        """Tokenized context of self at a point in time."""
        return TokenizedContext(
            tokens=self.prompt_tokens,
            idx_after_timestamp=self.idx_after_timestamp,
            context_num_msg=self.num_messages_included,
            truncated_num_msg=self.num_messages_truncated,
        )

    @property
    def prompt_tokens(self) -> list[int]:
        """Raw promp tokens at a point in time."""
        return reduce(lambda acc, part: acc + part.tokens, self.prompt_parts, [])

    @property
    def prompt_string(self) -> str:
        """Raw prompt string at a point in time."""
        return self.tokenizer.detokenize(self.prompt_tokens)

    @property
    def prompt_string_pretruncation(self) -> str:
        """Raw prompt string before truncation."""
        return reduce(
            lambda acc, part: acc + part.raw_string, self.prompt_parts_bak, ""
        )

    @property
    def total_active_tokens(self) -> int:
        """Total number of tokens in the context."""
        return self.num_total_tokens - self.num_tokens_truncated

    @monitor
    def _load_yaml(self, rendered_template: str) -> list[PromptPart]:
        """Load yaml from rendered template."""
        try:
            loaded_yaml = yaml.load(rendered_template, Loader=CSafeLoader)
        except Exception as ex:
            self._logger.error(
                f"### Hermes: Error loading yaml from rendered template {ex=}",
                exc_info=True,
            )
            raise ex

        return list(
            map(
                lambda x: PromptPart(**x),
                loaded_yaml,
            )
        )

    def _calculate_num_tokens_to_truncate(self):
        """Calculates the number of messages to truncate."""
        if self.truncation_step is None:
            self.truncation_step = Context.CACHE_FRIENDLY_TRUNCATION_STEP

        num_surplus_tokens = max(0, self.num_total_tokens - self.token_limit)
        return (
            math.ceil(num_surplus_tokens / self.truncation_step) * self.truncation_step
        )

    def _truncate(self):
        """Truncate messages from prompt_parts; modifies prompt_parts in place."""
        self._observe_context_metrics()
        if self.message_start_idx == -1:
            raise MessageStartIdxNotFound(
                f"Message start index not found: {self.message_start_idx=}"
            )

        if self.num_messages_truncated == 0:
            self._logger.info("No truncation needed.")
            return

        if self.num_messages_truncated == self.num_total_messages:
            self._logger.warn("Truncating all messages!")

        self.prompt_parts_bak = self.prompt_parts
        self.prompt_parts = (
            self.prompt_parts[: self.message_start_idx]
            + self.prompt_parts[self.message_start_idx + self.num_messages_truncated :]
        )

    # TODO: move this out of the wheel.
    def _observe_context_metrics(self):
        """Observe truncation metrics."""
        # TODO: use constants.
        Metrics().TOKEN_METRICS.labels(metric_type="total_tokens").observe(
            self.num_total_tokens
        )
        Metrics().TOKEN_METRICS.labels(metric_type="truncated_tokens").observe(
            self.num_tokens_truncated
        )
        Metrics().TOKEN_METRICS.labels(metric_type="active_tokens").observe(
            self.total_active_tokens
        )
        if self.num_total_pinned_message_tokens > 0:
            Metrics().TOKEN_METRICS.labels(
                metric_type="total_pinned_message_tokens"
            ).observe(self.num_total_pinned_message_tokens)

        Metrics().MESSAGE_METRICS.labels(metric_type="total_rendered_messages").observe(
            self.num_total_messages
        )
        Metrics().MESSAGE_METRICS.labels(metric_type="truncated_messages").observe(
            self.num_messages_truncated
        )
        Metrics().MESSAGE_METRICS.labels(metric_type="total_active_messages").observe(
            self.num_messages_included
        )

        if self.num_total_pinned_messages > 0:
            Metrics().MESSAGE_METRICS.labels(
                metric_type="truncated_messages_with_pinned"
            ).observe(self.num_messages_truncated)
            Metrics().MESSAGE_METRICS.labels(
                metric_type="total_active_messages_with_pinned"
            ).observe(self.num_messages_included)

    def _tokenize_part(self, prompt_part: PromptPart):
        prompt_part.tokens = self.tokenizer.tokenize(prompt_part.raw_string)
        self.num_total_tokens += len(prompt_part.tokens)
        if prompt_part.name.startswith("pinned_message"):
            self.num_total_pinned_message_tokens += len(prompt_part.tokens)

    def _clean_raw_string(self, prompt_part: PromptPart):
        # Cleanup whitespace, newlines and add whitespace where it is explicitly marked.
        prompt_part.raw_string = (
            prompt_part.raw_string.strip()
            .replace(Context.SPACE_MARKER, " ")
            .replace(Context.ESCAPED_NEWLINE, Context.NEWLINE)
            .replace(Context.ESCAPED_CARRIAGE_RETURN, Context.CARRIAGE_RETURN)
            .replace(Context.ESCAPED_SINGLE_QUOTE, Context.SINGLE_QUOTE)
        )

    def _maybe_extract_metadata_and_clean(self, idx: int, prompt_part: PromptPart):
        if prompt_part.name == Context.BOD_PART_NAME:
            self.idx_after_timestamp = len(prompt_part.tokens) + 1
            self.timestamp_str = prompt_part.raw_string.replace(Context.BOD, "")

        if prompt_part.name == Context.REPLY_PROMPT_PART_NAME:
            self.raw_reply_prompt = prompt_part.raw_string.replace(Context.BOM, "")

        if prompt_part.name.startswith("message"):
            if self.message_start_idx == -1:
                self.message_start_idx = idx
            self.num_total_messages += 1

        if prompt_part.name.startswith("pinned_message"):
            self.num_total_pinned_messages += 1
