from datetime import datetime, timedelta, timezone
import base64
import logging

from django.db import models
from django.dispatch import receiver
from specklepy.api.client import SpeckleClient
from google.cloud import logging as stackdriver

from gql import gql
from kube.apps import Kubernetes

logger = logging.getLogger('django')
stackdriver_client = stackdriver.Client(project="hack-space-dev")

OBFUSCATED_SECRET_VALUE = '******************'
B64_OBFUSCATED_SECRET_VALUE = base64.b64encode(
    OBFUSCATED_SECRET_VALUE.encode("ascii")).decode("ascii")
API_KEY_SECRET_NAME = 'speckle-api-key'


class Stream(models.Model):
    speckle_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)


class Bot(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50)
    description = models.CharField(max_length=200)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    webhook_id = models.CharField(max_length=30)
    triggers = models.JSONField()
    function_version = models.ForeignKey(
        'functions.FunctionVersion', on_delete=models.CASCADE)
    environment_variables = models.JSONField()
    environment_secrets = models.JSONField()

    @property
    def kubernetes_namespace(self):
        return self.owner.username

    @property
    def kubernetes_configmap(self):
        client = Kubernetes.get_client()
        return client.V1ConfigMap(
            api_version="v1",
            kind="ConfigMap",
            metadata=client.V1ObjectMeta(
                name=self.slug,
                namespace=self.kubernetes_namespace,
            ),
            data=self.environment_variables,
        )

    def upsert_kubernetes_configmap(self):
        v1 = Kubernetes.get_client().CoreV1Api()
        try:
            v1.read_namespaced_config_map(
                name=self.slug,
                namespace=self.kubernetes_namespace,
            )
            v1.patch_namespaced_config_map(
                name=self.slug,
                namespace=self.kubernetes_namespace,
                body=self.kubernetes_configmap,
            )
        except:
            v1.create_namespaced_config_map(
                namespace=self.kubernetes_namespace,
                body=self.kubernetes_configmap,
            )

    def delete_kubernetes_configmap(self):
        client = Kubernetes.get_client()
        kube = client.CoreV1Api()
        kube.delete_namespaced_config_map(
            namespace=self.kubernetes_namespace,
            name=self.slug,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=10)
        )

    @property
    def base64_encoded_secrets(self):
        secret = {}
        for k, v in self.environment_secrets.items():
            string_bytes = v.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            base64_string = base64_bytes.decode("ascii")
            secret[k] = base64_string
        return secret

    @property
    def kubernetes_secret(self):
        client = Kubernetes.get_client()
        return client.V1Secret(
            api_version="v1",
            kind="Secret",
            metadata=client.V1ObjectMeta(
                name=self.slug,
                namespace=self.kubernetes_namespace,
            ),
            data=self.base64_encoded_secrets,
        )

    def upsert_kubernetes_secret(self):
        client = Kubernetes.get_client()
        v1 = client.CoreV1Api()
        try:
            secret = v1.read_namespaced_secret(
                name=self.slug,
                namespace=self.kubernetes_namespace,
            )

            for k, v in self.base64_encoded_secrets.items():
                if v != B64_OBFUSCATED_SECRET_VALUE:
                    secret.data[k] = v

            for k in secret.data.keys():
                if k not in self.environment_secrets.keys():
                    del secret.data[k]

            v1.patch_namespaced_secret(
                name=self.slug,
                namespace=self.kubernetes_namespace,
                body=secret,
            )
        except Exception as err:
            logger.info(f'Failed to update secret: {err}')
            v1.create_namespaced_secret(
                namespace=self.kubernetes_namespace,
                body=self.kubernetes_secret,
            )

    def delete_kubernetes_secret(self):
        client = Kubernetes.get_client()
        kube = client.CoreV1Api()
        kube.delete_namespaced_secret(
            namespace=self.kubernetes_namespace,
            name=self.slug,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=10)
        )

    @property
    def image_pull_secret(self):
        return 'artifact-registry-secret'

    @property
    def knative_service(self):
        return {
            'apiVersion': 'serving.knative.dev/v1',
            'kind': 'Service',
            'metadata': {
                'name': self.slug,
                'namespace': self.kubernetes_namespace,
            },
            'spec': {
                'template': {
                    'spec': {
                        'imagePullSecrets': [{
                            'name': self.image_pull_secret
                        }],
                        'containers': [{
                            'image': self.function_version.container_image_uri,
                            'envFrom': [{
                                'secretRef': {
                                    'name': self.slug
                                }
                            }, {
                                'configMapRef': {
                                    'name': self.slug
                                }
                            }],
                            'env': [{
                                'name': 'FUNCKLE_USER_TOKEN',
                                'valueFrom': {
                                    'secretKeyRef': {
                                        'name': API_KEY_SECRET_NAME,
                                        'key': API_KEY_SECRET_NAME,
                                    }
                                }
                            }],
                        }]
                    }
                }
            }
        }

    def get_kservice(self):
        kube = Kubernetes.get_client().CustomObjectsApi()
        return kube.get_namespaced_custom_object(
            group='serving.knative.dev',
            version='v1',
            namespace=self.kubernetes_namespace,
            plural='services',
            name=self.slug
        )

    def upsert_kservice(self):
        kube = Kubernetes.get_client().CustomObjectsApi()
        try:
            self.get_kservice()
            kube.patch_namespaced_custom_object(
                group='serving.knative.dev',
                version='v1',
                namespace=self.kubernetes_namespace,
                plural='services',
                name=self.slug,
                body=self.knative_service,
            )
        except:
            kube.create_namespaced_custom_object(
                group='serving.knative.dev',
                version='v1',
                namespace=self.kubernetes_namespace,
                plural='services',
                body=self.knative_service
            )

    def delete_kservice(self):
        client = Kubernetes.get_client()
        kube = client.CustomObjectsApi()
        kube.delete_namespaced_custom_object(
            group='serving.knative.dev',
            version='v1',
            namespace=self.kubernetes_namespace,
            plural='services',
            name=self.slug,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=10)
        )

    def get_logs(self):
        # Use pod label: serving.knative.dev/serviceUID=<uid-of-knative-service>
        kservice = self.get_kservice()
        uid = kservice['metadata']['uid']
        last_hour = datetime.now(timezone.utc) - timedelta(hours=1)
        time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

        query = ('resource.type="k8s_container"'
                 f' AND labels."k8s-pod/serving_knative_dev/serviceUID"="{uid}"'
                 ' AND resource.labels.container_name="user-container"'
                 f' AND timestamp>="{last_hour.strftime(time_format)}"')

        # Cloud Logging API Call
        logs = []
        for log in stackdriver_client.list_entries(filter_=query):
            logs.append(
                f'{log.timestamp.strftime("%Y-%m-%d %H:%M:%S")} -- {log.payload}'
            )
        return logs

    @staticmethod
    def generate_url(slug: str, username: str):
        return f'https://{slug}.{username}.funckle.nerd-extraordinaire.com'

    @staticmethod
    def create_webhook(client: SpeckleClient, stream_id, url, triggers, secret, description) -> str:
        query = gql(
            """
                mutation($webhook: WebhookCreateInput!) {
                    webhookCreate(webhook: $webhook)
                }
            """
        )

        params = {
            "webhook": {"streamId": stream_id, "url": url, "triggers": triggers, "secret": secret, "description": description, "enabled": True}
        }

        return client.stream.make_request(
            query=query, params=params, return_type="webhookCreate", parse_response=False
        )

    @staticmethod
    def update_webhook(client: SpeckleClient, stream_id, webhook_id, url, triggers, secret) -> str:
        query = gql(
            """
                mutation($webhook: WebhookUpdateInput!) {
                    webhookUpdate(webhook: $webhook)
                }
            """
        )

        params = {
            "webhook": {"streamId": stream_id, "id": webhook_id, "url": url, "triggers": triggers, "secret": secret, "enabled": True}
        }

        return client.stream.make_request(
            query=query, params=params, return_type="webhookUpdate", parse_response=False
        )

    @staticmethod
    def delete_webhook(client: SpeckleClient, stream_id, webhook_id):
        query = gql(
            """
                mutation($webhook: WebhookDeleteInput!) {
                    webhookDelete(webhook: $webhook)
                }
            """
        )

        params = {"webhook": {"streamId": stream_id, "id": webhook_id}}

        return client.stream.make_request(
            query=query, params=params, return_type="webhookDelete", parse_response=False
        )


@receiver(models.signals.pre_save, sender=Bot)
def upsert_kubernetes_resources(sender, instance: Bot, **kwargs):
    """
    Upserts a configmap, secret and knative service
    """
    if instance.environment_variables is None:
        instance.environment_variables = {}
    instance.upsert_kubernetes_configmap()

    if instance.environment_variables is None:
        instance.environment_secrets = {}
    instance.upsert_kubernetes_secret()
    for k in instance.environment_secrets.keys():
        instance.environment_secrets[k] = OBFUSCATED_SECRET_VALUE

    instance.upsert_kservice()


@receiver(models.signals.post_delete, sender=Bot)
def delete_kubernetes_resources(sender, instance: Bot, **kwargs):
    """
    Deletes configmap, secret and knative service
    """
    try:
        instance.delete_kservice()
    except Exception as err:
        logger.error(f'Failed to delete knative service: {err}')

    try:
        instance.delete_kubernetes_configmap()
    except Exception as err:
        logger.error(f'Failed to delete configmap: {err}')

    try:
        instance.delete_kubernetes_secret()
    except Exception as err:
        logger.error(f'Failed to delete secret: {err}')
