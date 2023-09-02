import os

from specklepy.api.client import SpeckleClient
from specklepy.core.api.models import Stream
from funckle.function.handler import webhook_handler
from funckle.function.events import WebhookPayload

from slack_sdk.webhook import WebhookClient

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", None)


@webhook_handler(validate_webhook=True)
def webhook(webhook: WebhookPayload, client: SpeckleClient):
    print(f'Webhook received: {webhook}')
    if SLACK_WEBHOOK_URL is None:
        raise Exception("SLACK_WEBHOOK_URL is not set")

    slack = WebhookClient(SLACK_WEBHOOK_URL)

    stream: Stream = client.stream.get(webhook.streamId)
    user = client.user.get(webhook.userId)

    res = slack.send_dict(
        {
            'username': user.name,
            'icon_url': user.avatar,
            'text': (
                f"Stream event: {webhook.event.event_name}"
                f"\nStream: <https://speckle.xyz/streams/{stream.id}|{stream.name}>"
                f"\nMessage: {webhook.activityMessage}"
            )
        }
    )

    if res.status_code != 200:
        print(f'Failed to send slack webhook: {res.status_code} {res.text}')
        raise Exception("Slack webhook failed")

    print(f'Slack webhook sent: {res.status_code} {res.text}')
    return "OK"
