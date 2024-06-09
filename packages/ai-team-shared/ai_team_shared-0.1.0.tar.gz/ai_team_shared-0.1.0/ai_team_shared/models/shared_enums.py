from enum import Enum


class ModelNameLLM(str, Enum):
    GPT_3 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4-turbo-preview"
    CLAUDE_3_0 = "claude-3-haiku-20240307"
    CLAUDE_3_1 = "claude-3-sonnet-20240229"
    CLAUDE_3_2 = "claude-3-opus-20240229"


class TaskType(str, Enum):
    # Coder
    FRONTEND = "FRONTEND"
    SVC_IMPL = "SVC_IMPL"
    UNIT_TEST = "UNIT_TEST"
    INTERFACE = "INTERFACE"
    DATA_MODEL = "DATA_MODEL"

    # CTO
    SCOPED_TASK = "SCOPED_TASK"
    REQUIREMENT = "REQUIREMENT"
    ARCHITECTURE = "ARCHITECTURE"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    PROTOTYPE = "PROTOTYPE"

    # CEO
    ROADMAP = "ROADMAP"
    OKR = "OKR"

    # COO
    COMPLIANCE = "COMPLIANCE"

    # General
    DOCUMENTATION = "DOCUMENTATION"

    # Special
    UNDEFINED = "UNDEFINED"
