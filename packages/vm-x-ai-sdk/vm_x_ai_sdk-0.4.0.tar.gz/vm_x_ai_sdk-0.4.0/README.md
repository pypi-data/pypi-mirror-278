# VM-X SDK for Python

## Description

VM-X AI SDK client for Python

## Installation

```bash
pip install vm-x-ai-sdk
```

```bash
poetry add vm-x-ai-sdk
```

## Usage

```python

from vmxai import CompletionRequest, RequestMessage, VMXClient, VMXClientOAuth

client = VMXClient(
    domain="env-abc123.clnt.dev.vm-x.ai",
    environment_id="env-abc123",
    workspace_id="ws-abc123",
    # Authentication options
    # OAuth Client credentials
    auth=VMXClientOAuth(
        client_id="abc123",
        client_secret="abc123",
    ),
    # Or API Key
    api_key="abc123",
)

# Streaming
streaming_response = client.completion(
    request=CompletionRequest(
        resource="resource1-openai-gpt-3-5-turbo",
        workload="high1",
        messages=[
            RequestMessage(
                role="user",
                content="Hey there!",
            )
        ],
    ),
)

for message in streaming_response:
    print(message.message)


# Non-Streaming
response = client.completion(
    request=CompletionRequest(
        resource="resource1-openai-gpt-3-5-turbo",
        workload="high1",
        messages=[
            RequestMessage(
                role="user",
                content="Hey there!",
            )
        ],
    ),
    stream=False,
)

print(response.message)

```

## [Change Log](./CHANGELOG.md)
