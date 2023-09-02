import flask
import hmac
from .events import RequestPayload
from .settings import settings

def validate_webhook_payload(request: flask.Request):
    signature_from_header = request.headers.get('X-Webhook-Signature', '')
    expected_signature = hmac.new(settings.webhook_secret.encode(), request.data, 'sha256').hexdigest()
    if not hmac.compare_digest(expected_signature, signature_from_header):
        raise Exception('Invalid signature')

def webhook_handler(validate_webhook: bool = True):
    def inner_decorator(f):
        def wrapped(request: flask.Request) -> flask.Response:
            if validate_webhook:
                try:
                    validate_webhook_payload(request)
                except Exception as e:
                    print(e)
                    return flask.Response(str(e), status=400)

            try:
                webhook = RequestPayload.model_validate_json(request.data)
                speckle_client = settings.speckle_client()
            except Exception as e:
                print(e)
                return flask.Response(str(e), status=400)

            try:
                return f(
                    webhook=webhook.payload,
                    client=speckle_client
                )
            except Exception as e:
                print(e)
                return flask.Response(str(e), status=500)

        return wrapped
    
    return inner_decorator