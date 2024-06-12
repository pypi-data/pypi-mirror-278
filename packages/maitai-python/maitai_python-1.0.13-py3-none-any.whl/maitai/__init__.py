import os

from maitai._azure import MaitaiAsyncAzureOpenAIClient as AsyncAzureOpenAI, MaitaiAzureOpenAIClient as AzureOpenAI
from maitai._evaluator import Evaluator as Evaluator
from maitai._inference import Inference as Inference
from maitai._openai import Chat, MaitaiOpenAIClient as OpenAI
from maitai._openai_async import MaitaiAsyncOpenAIClient as AsyncOpenAI

chat = Chat()


def initialize(api_key):
    from maitai._config import config
    config.initialize(api_key)


if os.environ.get("MAITAI_API_KEY") and os.environ.get("MAITAI_ENV") != "development":
    initialize(os.environ.get("MAITAI_API_KEY"))
