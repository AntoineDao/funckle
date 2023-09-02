# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Quickstart

Install the package and run the function locally:

```bash
# Install the package
pip install -r requirements.txt
```

Login to Funckle. This open a new browser window and after logging in will create a `.funckle` file in your home directory to store your credentials:

```bash
# Login to Funckle
funckle login
```

Deploy the function to Funckle:

```bash
# Install the package
funckle deploy --version 0.1.0
```

## Usage

You must always use the `webhook` function as the entrypoint to your code. This function should be defined in the `main.py` file. 

This function will be called by Funckle when a new event is received. We have provided a helpful wrapper function that parses and validates webhook payloads. 

```python
from specklepy.api.client import SpeckleClient
from specklepy.core.api.models import Stream
from funckle.function.handler import webhook_handler
from funckle.function.events import WebhookPayload

@webhook_handler(validate_webhook=True)
def webhook(webhook: WebhookPayload, client: SpeckleClient):
    auth_context = client.active_user.get()
    print(f"Authenticated as {auth_context.name}")
    
    stream: Stream = client.stream.get(webhook.streamId)
    message = f"Hello, validated webhook for stream: {stream.name}!!!!"
    print(message)

    return message

```

You could also choose to handle the webhook payload yourself:

```python
import flask

def webhook(request: flask.Request) -> flask.Response
    webhook_payload = request.json
    webhook_signature = request.headers.get("X-Webhook-Signature")

    # Implement your own validation logic here
    ...

    stream_id = webhook_payload["streamId"]

    return f"Hello {streamId}!!!!"
```

## Function Configuration

You can configure your function by editing the `.funckle.json` file. The configuration options define which function this package it deployed to and adds some helpful metadata. This file contains the following configuration options:

```json
{
    "name": "New Function",
    "description": "A new function",
    "sourceLocation": "https://github.com/funckle/new-function",
}
```