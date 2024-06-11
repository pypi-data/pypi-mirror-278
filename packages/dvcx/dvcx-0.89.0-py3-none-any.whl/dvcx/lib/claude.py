import json
from json import JSONDecodeError
from typing import Literal

import anthropic
from anthropic.types import Usage
from anthropic.types.message import Message
from pydantic import Field

from dvcx.lib.feature import Feature
from dvcx.lib.feature_types import FeatureLike, pydantic_to_feature
from dvcx.lib.feature_udf import FeatureAggregator, FeatureMapper
from dvcx.lib.file import FileInfo, TextFile

default_model_name = "claude-3-haiku-20240307"
DEFAULT_OUTPUT_TOKENS = 1024

MessageFeature = pydantic_to_feature(Message)
UsageFeature = pydantic_to_feature(Usage)


class Claude(MessageFeature):  # type: ignore[valid-type,misc]
    error: str = ""


class Rating(Feature):
    status: Literal["Success", "Failure"] = "Failure"
    explanation: str = ""
    usage: UsageFeature = UsageFeature(input_tokens=0, output_tokens=0)  # type: ignore[valid-type,call-arg]
    error: str = ""


class Summary(Feature):
    reasons: list[str] = Field(default_factory=list)
    usage: UsageFeature = UsageFeature(input_tokens=0, output_tokens=0)  # type: ignore[valid-type,call-arg]
    error: str = ""


class ClaudeClient:
    def __init__(
        self,
        prompt,
        messages=None,
        model_name="",
        api_key=None,
        max_retries=5,
        **kwargs,
    ):
        self.prompt = prompt
        self.model_name = model_name
        self.messages = messages
        self.api_key = api_key
        self.max_retries = max_retries
        self.kwargs = kwargs
        self.model = None

        if not self.messages:
            self.messages = []
        if "max_tokens" not in self.kwargs:
            self.kwargs["max_tokens"] = DEFAULT_OUTPUT_TOKENS

    def bootstrap(self):
        self.model = anthropic.Anthropic(api_key=self.api_key)
        if self.max_retries:
            self.model = self.model.with_options(max_retries=self.max_retries)

    def teardown(self):
        self.model.close()
        self.model = None

    def llm_call(self, text):
        try:
            response = self.model.messages.create(  # type: ignore[attr-defined]
                model=self.model_name,
                system=self.prompt,
                messages=[{"role": "user", "content": text}, *self.messages],
                **self.kwargs,
            )

            return Claude(**response.model_dump())
        except Exception as exc:  # noqa: BLE001
            return Claude(
                id="",
                content=[],
                model="",
                role="assistant",
                type="message",
                usage={"input_tokens": 0, "output_tokens": 0},
                error=str(exc),
            )

    @staticmethod
    def get_rating(claude: Claude):
        if claude.error:
            response = Rating(status="Failure", usage=claude.usage, error=claude.error)
        elif len(claude.content) > 0:
            text = claude.content[0].text
            try:
                j = json.loads(text)
                response = Rating(**j)
                response.usage = claude.usage
            except JSONDecodeError as exc:
                response = Rating(
                    error=f"json parsing error '{text}': {exc!s}", usage=claude.usage
                )
        else:
            response = Rating(
                status="Failure", error="no responses", usage=claude.usage
            )
        return response


class ClaudeMessage(ClaudeClient, FeatureMapper):
    def __init__(
        self,
        data: FeatureLike = TextFile,
        **kwargs,
    ):
        ClaudeClient.__init__(self, **kwargs)
        FeatureMapper.__init__(self, data, Claude)

    def process(self, data):
        return self.llm_call(data.get_value())


class TextAnalytics(ClaudeClient, FeatureMapper):
    """Run system prompt on records one-by-one and return responses in a column"""

    def __init__(self, data: FeatureLike = TextFile, **kwargs):
        ClaudeClient.__init__(self, **kwargs)
        FeatureMapper.__init__(self, data, Rating)

    def process(self, data):
        claude = self.llm_call(data.get_value())
        return self.get_rating(claude)


class AggregateTextAnalytics(ClaudeClient, FeatureAggregator):
    """Run the system prompt on all records and return one response"""

    def __init__(self, data: FeatureLike = TextFile, **kwargs):
        ClaudeClient.__init__(self, **kwargs)
        FeatureAggregator.__init__(self, data, [FileInfo, Summary])

    def process(self, args):
        all_texts = "\n=====\n".join(data.get_value() for data in args)
        claude = self.llm_call(all_texts)

        if claude.error == "":
            text = claude.content[0].text
            try:
                j = json.loads(text)
                if isinstance(j, list):
                    result = Summary(reasons=j, usage=claude.usage)
                else:
                    result = Summary(
                        error=f"result is not list but '{j}'", usage=claude.usage
                    )
            except JSONDecodeError as exc:
                result = Summary(
                    error=f"json parsing error '{text}': {exc!s}", usage=claude.usage
                )
        else:
            result = Summary(error=claude.error, usage=claude.usage)

        yield FileInfo(name="", vtype="claude-agg"), result
