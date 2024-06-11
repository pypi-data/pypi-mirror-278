"""C.AI specific constants for the Hermes engine."""

NARRATOR_NAME = "narrator"
DEFAULT_USERNAME = "user"
VALID_PROMPT_STRING_PATTERNS = [
    r"^<\|beginningofdialog\|>(\d{4} \d{2} \d{2} (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) \d{2} \d{2} [\w\W]+):",
    r"^(?!.*<\|endofmessage\|>(?!<\|beginningofmessage\|>))",
]
TIMEOUT_SECONDS = 60
ROUTE_COOKIE_NAME = "route"
MAX_CONTINUATIONS = 10
N_CODE = ord("\n")
PROMPT_PRETRUNCATION = "prompt_pretruncation"
PROMPT_DIFF_MESSAGE_TYPE = "prompt_diff"
LEGACY_PROMPT_MESSAGE_TYPE = "legacy_prompt"
TRUNCATION_STEPS_CHOICES = [250, 500, 750, 1000, 1250, 1500]
