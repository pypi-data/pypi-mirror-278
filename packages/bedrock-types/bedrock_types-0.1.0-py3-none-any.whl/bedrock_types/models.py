from pydantic import BaseModel, Field, Json, Base64Bytes
from typing import Literal, Optional, Any, List, Dict


class ImageSource(BaseModel):
    # ref https://docs.pydantic.dev/2.0/usage/types/encoded/#base64-encoding-support
    bytes: Optional[Base64Bytes]


# ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ImageBlock.html
class ImageBlock(BaseModel):
    format: Literal["png", "jpeg", "gif", "webp"]
    source: ImageSource


class ToolResultContentBlock(BaseModel):
    image: Optional[ImageBlock] | None
    result_json: Optional[Json[Any]] = Field(alias="json")
    text: str


# ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ToolResultBlock.html
class ToolResultBlock(BaseModel):
    content: List[ToolResultContentBlock]
    toolUseId: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    status: Literal["success", "error"]


class ToolUseBlock(BaseModel):
    input: Json[Any]
    name: str = Field(pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$")
    toolUseId: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")


# ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ContentBlock.html
class ContentBlock(BaseModel):
    image: Optional[ImageBlock] = None
    text: Optional[str]
    toolResult: Optional[ToolResultBlock] = None
    toolUse: Optional[ToolUseBlock] = None


# ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Message.html
class Message(BaseModel):
    content: List[ContentBlock]
    role: Literal["user", "assistant"]


# ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseOutput.html
class ConverseOutput(BaseModel):
    message: Message


class ConverseMetrics(BaseModel):
    latencyMs: int


class TokenUsage(BaseModel):
    inputTokens: int
    outputTokens: int
    totalTokens: int


# ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html
class ConverseResponse(BaseModel):
    # basically HTTP Headers related staff, not likely to be malfored
    ResponseMetadata: Any
    additionalModelResponseFields: Dict[str, Any] = Field(
        None, alias="additional_model_response_fields"
    )
    metrics: ConverseMetrics
    output: ConverseOutput
    stopReason: Literal[
        "end_turn", "tool_use", " max_tokens", "stop_sequence", "content_filtered"
    ]
    usage: TokenUsage


# ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InferenceConfiguration.html
class InferenceConfig(BaseModel):
    max_tokens: Optional[int] = Field(1024, alias="maxTokens", ge=1)
    stop_sequences: Optional[List[str]] = Field(None, alias="stopSequences")
    temperature: Optional[float] = None
    top_p: Optional[float] = Field(None, alias="topP")


class SystemContentBlock(BaseModel):
    text: Optional[str] = Field(None, min_length=1)


### Stream Response
class ToolUseBlockDelta(BaseModel):
    input: str


class ToolUseBlockStart(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$", min_length=1, max_length=64)
    toolUseId: str = Field(pattern=r"^[a-zA-Z0-9_-]+$", min_length=1, max_length=64)


# ref: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ContentBlockDelta.html
class ContentBlockDelta(BaseModel):
    text: Optional[str] = None
    toolUse: Optional[ToolUseBlockDelta] = None


class ContentBlockDeltaEvent(BaseModel):
    contentBlockIndex: int = Field(min=0)
    delta: ContentBlockDelta


class ContentBlockStart(BaseModel):
    toolUse: Optional[ToolUseBlockStart]


class ContentBlockStartEvent(BaseModel):
    contentBlockIndex: int = Field(min=0)
    start: ContentBlockStart


class ContentBlockStopEvent(BaseModel):
    contentBlockIndex: int = Field(min=0)


class MessageStartEvent(BaseModel):
    role: Literal["user", "assistant"]


class MessageStopEvent(BaseModel):
    stopReason: Literal[
        "end_turn", "tool_use", "max_tokens", "stop_sequence", "content_filtered "
    ]
    additionalModelResponseFields: Optional[Any] = None


class ConverseStreamMetrics(BaseModel):
    latencyMs: int


class ConverseStreamMetadataEvent(BaseModel):
    metrics: ConverseStreamMetrics
    usage: TokenUsage


class ConverseStreamOutput(BaseModel):
    contentBlockDelta: Optional[ContentBlockDeltaEvent] = None
    contentBlockStart: Optional[ContentBlockStartEvent] = None
    contentBlockStop: Optional[ContentBlockStopEvent] = None
    internalServerException: Optional[Any] = None
    messageStart: Optional[MessageStartEvent] = None
    messageStop: Optional[MessageStopEvent] = None
    metadata: Optional[ConverseStreamMetadataEvent] = None
    modelStreamErrorException: Optional[Any] = None
    throttlingException: Optional[Any] = None
    validationException: Optional[Any] = Field(default="400")
