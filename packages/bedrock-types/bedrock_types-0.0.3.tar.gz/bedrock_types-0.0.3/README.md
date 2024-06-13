# Amazon Bedrock Converse API Data Types

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