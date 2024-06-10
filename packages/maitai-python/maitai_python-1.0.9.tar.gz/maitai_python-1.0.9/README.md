# Quickstart

Full docs can be found at https://docs.trymaitai.ai

## Configure your application in the Maitai portal

From the [Maitai Portal](https://portal.trymaitai.ai/), click the `+ New Application` button to create your first
application.

Fill out your application details, and note the `Application Reference` - you'll need that later

## Create your first sentinel

Maitai will analyze your application and automatically create sentinels for you over time. However, if you want to
enable governance immediately, you can manually create sentinels as well.

Find your application in the portal and click the `+` button to create a new sentinel.

## Installation

Install the Maitai SDK:

```bash
pip install maitai-python
```

## Implementation

Integrating Maitai into your application requires minimal code changes

```python
import maitai as openai

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Generate numbers 1-10"},
]

response = openai.chat.completions.create(
    messages=messages,
    model="gpt-4",
    session_id="YOUR_SESSION_ID",
    action_type="NUMBER_GENERATOR",
    application_ref_name="YOUR_APPLICATION_REF_NAME",
)
```