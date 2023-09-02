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
