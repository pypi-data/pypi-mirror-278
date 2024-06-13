# Amazon Bedrock Converse API Data Types

[![PyPI version](https://badge.fury.io/py/bedrock-types.svg)](https://badge.fury.io/py/bedrock-types)
[![release](https://github.com/hustshawn/bedrock-types/actions/workflows/python-publish.yml/badge.svg)](https://github.com/hustshawn/bedrock-types/actions/workflows/python-publish.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bedrock-types.svg)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)




This project is a [Pydantic](https://github.com/pydantic/pydantic) implementation of [Amazon Bedrock Runtime Converse API Data Types](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Types_Amazon_Bedrock_Runtime.html).


## Example Usage

```python
from bedrock_types import ConverseResponse

...

response = client.converse(
    modelId=model_id,
    messages=messages,
    system=system_prompts,
    inferenceConfig=inference_config,
    additionalModelRequestFields=additional_model_fields,
)

parsed = ConverseResponse.model_validate(response)
print(parsed.model_dump_json(indent=4, exclude_unset=True))
print(parsed.ResponseMetadata)

```
Output
```
ResponseMetadata={'RequestId': '427c73bb-df2d-4c1a-8744-db1b5b3c4897', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 13 Jun 2024 09:11:25 GMT', 'content-type': 'application/json', 'content-length': '247', 'connection': 'keep-alive', 'x-amzn-requestid': '427c73bb-df2d-4c1a-8744-db1b5b3c4897'}, 'RetryAttempts': 0} additionalModelResponseFields=None metrics=ConverseMetrics(latencyMs=740) output=ConverseOutput(message=Message(content=[ContentBlock(image=None, text="Why don't scientists trust atoms? Because they make up everything!", toolResult=None, toolUse=None)], role='assistant')) stopReason='end_turn' usage=TokenUsage(inputTokens=22, outputTokens=16, totalTokens=38)
{
    "ResponseMetadata": {
        "RequestId": "427c73bb-df2d-4c1a-8744-db1b5b3c4897",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "date": "Thu, 13 Jun 2024 09:11:25 GMT",
            "content-type": "application/json",
            "content-length": "247",
            "connection": "keep-alive",
            "x-amzn-requestid": "427c73bb-df2d-4c1a-8744-db1b5b3c4897"
        },
        "RetryAttempts": 0
    },
    "metrics": {
        "latencyMs": 740
    },
    "output": {
        "message": {
            "content": [
                {
                    "text": "Why don't scientists trust atoms? Because they make up everything!"
                }
            ],
            "role": "assistant"
        }
    },
    "stopReason": "end_turn",
    "usage": {
        "inputTokens": 22,
        "outputTokens": 16,
        "totalTokens": 38
    }
}
{'RequestId': '427c73bb-df2d-4c1a-8744-db1b5b3c4897', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 13 Jun 2024 09:11:25 GMT', 'content-type': 'application/json', 'content-length': '247', 'connection': 'keep-alive', 'x-amzn-requestid': '427c73bb-df2d-4c1a-8744-db1b5b3c4897'}, 'RetryAttempts': 0}
```