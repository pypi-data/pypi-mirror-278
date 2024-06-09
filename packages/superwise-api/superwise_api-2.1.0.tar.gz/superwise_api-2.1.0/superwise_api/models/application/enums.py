from enum import Enum


class Role(str, Enum):
    HUMAN = "human"
    AI = "ai"


class ModelProvider(str, Enum):
    OPENAI = "OpenAI"
    GOOGLE = "GoogleAI"
    VERTEX_AI_MODEL_GARDEN = "VertexAIModelGarden"


class OpenAIModelVersion(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_1106 = "gpt-3.5-turbo-1106"
    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_4 = "gpt-4"
    GPT_4_VISION_PREVIEW = "gpt-4-vision-preview"
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"


class GoogleModelVersion(str, Enum):
    GEMINI_PRO = "gemini-pro"
    TEXT_BISON_001 = "models/text-bison-001"


class VertexAIModelGardenVersion(str, Enum):
    PLACEHOLDER = "placeholder"
