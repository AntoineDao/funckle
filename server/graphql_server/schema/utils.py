from django.contrib.auth.models import User
from specklepy.api.client import SpeckleClient


def get_speckle_client(info) -> SpeckleClient:
    return info.context.speckle_client


def get_auth_user(info) -> User:
    return info.context.user
