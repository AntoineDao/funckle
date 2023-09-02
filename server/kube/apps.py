from django.apps import AppConfig
import os
from kubernetes import config, client


KUBE_CONFIG = os.environ.get('KUBE_CONFIG', 'local')


class Kubernetes:

    _client_authenticated = False

    @classmethod
    def get_client(cls):
        if not cls._client_authenticated:
            if KUBE_CONFIG == 'local':
                config.load_kube_config()
            elif KUBE_CONFIG == 'in-cluster':
                config.load_incluster_config()
            cls._client_authenticated = True
        return client


class KubeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kube'
