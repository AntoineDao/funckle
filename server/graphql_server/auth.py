import base64

from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from specklepy.api.client import SpeckleClient

from django.db import models
from django.dispatch import receiver

from kube.apps import Kubernetes
from bots.models import API_KEY_SECRET_NAME

PREFIX = "Bearer"
AUTH_HEADER_NAME = "HTTP_AUTHORIZATION"


def get_http_authorization(request):
    auth = request.META.get(AUTH_HEADER_NAME, "").split()

    if len(auth) != 2 or auth[0].lower() != PREFIX.lower():
        return None
    return auth[1]


def upsert_namespace(namespace: str):
    client = Kubernetes.get_client()
    v1 = client.CoreV1Api()
    try:
        v1.read_namespace(
            name=namespace,
        )
    except:
        v1.create_namespace(
            body=client.V1Namespace(
                api_version="v1",
                kind="Namespace",
                metadata=client.V1ObjectMeta(
                    name=namespace,
                ),
            )
        )


def delete_namespace(namespace: str):
    client = Kubernetes.get_client()
    v1 = client.CoreV1Api()
    try:
        v1.delete_namespace(
            name=namespace,
        )
    except:
        pass


def upsert_api_key_secret(namespace: str, api_key: str):
    client = Kubernetes.get_client()
    v1 = client.CoreV1Api()
    encoded_api_key = base64.b64encode(api_key.encode('ascii')).decode('ascii')
    try:
        secret = v1.read_namespaced_secret(
            name=API_KEY_SECRET_NAME,
            namespace=namespace,
        )
        secret.data[API_KEY_SECRET_NAME] = encoded_api_key
        v1.replace_namespaced_secret(
            name=API_KEY_SECRET_NAME,
            namespace=namespace,
            body=secret,
        )
    except:
        v1.create_namespaced_secret(
            namespace=namespace,
            body=client.V1Secret(
                api_version="v1",
                kind="Secret",
                metadata=client.V1ObjectMeta(
                    name=API_KEY_SECRET_NAME,
                ),
                data={
                    API_KEY_SECRET_NAME: encoded_api_key,
                },
            )
        )


@receiver(models.signals.post_save, sender=User)
def create_kubernetes_namespace(sender, instance: User, **kwargs):
    """
    Create namsepace for the user
    """
    upsert_namespace(instance.username)


@receiver(models.signals.post_delete, sender=User)
def delete_kubernetes_resources(sender, instance: User, **kwargs):
    """
    Delete namsepace for the user
    """
    delete_namespace(instance.username)


class SpeckleBackend(BaseBackend):

    def __init__(self):
        self.has_authenticated = False
        self.cached_allow_any = set()

    def authenticate_context(self, info, **kwargs):
        if self.has_authenticated:
            return False

        self.has_authenticated = True
        return True

    def resolve(self, next, root, info, **kwargs):
        context = info.context

        auth_token = get_http_authorization(context)

        if self.authenticate_context(info, **kwargs):
            user = authenticate(request=context, token=auth_token)

            if user is not None:
                context.user = user

        return next(root, info, **kwargs)

    def authenticate(self, request, token=None):
        request.speckle_client = SpeckleClient(host='speckle.xyz')
        if token is None:
            # token = '056c1eba26fda7f35c7f42f56faefd22acfda74df9'
            return None

        request.speckle_client.authenticate_with_token(token)
        speckle_user = request.speckle_client.active_user.get()

        try:
            user = User.objects.get(
                username=speckle_user.id,
            )
        except User.DoesNotExist:
            # Create a new user. There's no need to set a password
            # because only the password from settings.py is checked.
            if speckle_user.avatar is None or len(speckle_user.avatar) >= 150:
                speckle_user.avatar = 'https://robohash.org/' + speckle_user.id
            if speckle_user.name is None:
                speckle_user.name = speckle_user.id

            user = User(
                username=speckle_user.id,
                email=speckle_user.email,
                first_name=speckle_user.name,
                last_name=speckle_user.avatar,
            )
            user.save()
        upsert_api_key_secret(user.username, token)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
