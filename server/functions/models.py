import logging

from django.db import models
from django.dispatch import receiver
from django.core.files.base import ContentFile
from kube.apps import Kubernetes

logger = logging.getLogger('django')

TEKTON_PRIMARY_KEY_ANNOTATION = 'function.funckle.io/pk'
PIPELINE_RUN_NAMESPACE = 'funckle'


class Function(models.Model):

    class Meta:
        unique_together = ('owner', 'slug')

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.CharField(max_length=200)
    readme = models.TextField(null=True, blank=True)
    source_location = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def namespace(self):
        return self.owner.username


class FunctionVersion(models.Model):

    PENDING = 'PENDING'
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    UNKNOWN = 'UNKNOWN'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'

    STATUS = (
        (PENDING, 'Pending'),
        (STARTED, 'Started'),
        (RUNNING, 'Running'),
        (UNKNOWN, 'Unknown'),
        (SUCCEEDED, 'Succeeded'),
        (FAILED, 'Failed'),
    )

    class Meta:
        unique_together = ('function', 'version')

    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    version = models.CharField(max_length=10)
    package = models.FileField(upload_to='functions/')
    status = models.CharField(choices=STATUS, default=PENDING, max_length=20)
    build_logs = models.FileField(
        upload_to='functions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def pipeline_name(self):
        return f'pipeline-{self.pk}'
        # return f'pipeline-{self.function.namespace}-{self.function.slug}-{self.version}'

    @property
    def container_image_registry(self):
        return 'europe-west2-docker.pkg.dev'

    @property
    def container_image(self):
        return f'hack-space-dev/funckle-user-functions/{self.function.namespace}/{self.function.slug}:{self.version}'

    @property
    def container_image_uri(self):
        return f'{self.container_image_registry}/{self.container_image}'

    @property
    def package_file_path(self):
        return f'{self.function.namespace}/{self.function.slug}/{self.version}/package.tar.gz'

    @property
    def build_logs_file_path(self):
        return f'{self.function.namespace}/{self.function.slug}/{self.version}/build-logs.txt'

    @property
    def pipeline(self):
        v1 = Kubernetes.get_client().CustomObjectsApi()
        return v1.get_namespaced_custom_object(
            group='tekton.dev',
            version='v1beta1',
            namespace=PIPELINE_RUN_NAMESPACE,
            plural='pipelineruns',
            name=self.pipeline_name
        )

    @property
    def pipeline_status(self):
        return self.pipeline['status']['conditions'][0]['status']

    @property
    def build_logs_text(self):
        if self.build_logs:
            return self.build_logs.read().decode('utf-8')
        return ''

    def save_build_logs(self):
        # List pods with label tekton.dev/pipelineRun=build-pipeline-run and tekton.dev/pipelineTask=build
        v1 = Kubernetes.get_client().CoreV1Api()
        pods = v1.list_namespaced_pod(
            namespace=PIPELINE_RUN_NAMESPACE,
            label_selector=f'tekton.dev/pipelineRun={self.pipeline_name},tekton.dev/pipelineTask=build',
        )
        if len(pods.items) == 0:
            return "No logs available"
        pod = pods.items[0]
        logs = v1.read_namespaced_pod_log(
            name=pod.metadata.name,
            namespace=PIPELINE_RUN_NAMESPACE,
            container='step-create',
        )
        self.build_logs.save(self.build_logs_file_path,
                             ContentFile(bytes(logs, 'utf-8')), save=True)

    def create_build_pipeline(self):
        client = Kubernetes.get_client()
        v1 = client.CustomObjectsApi()
        v1.create_namespaced_custom_object(
            group='tekton.dev',
            version='v1beta1',
            # TODO: parametrise thise value
            namespace=PIPELINE_RUN_NAMESPACE,
            plural='pipelineruns',
            body={
                "apiVersion": "tekton.dev/v1beta1",
                "kind": "Pipeline",
                "metadata": {
                    "name": self.pipeline_name,
                    "labels": {
                        "tekton.dev/pipeline": "funckle-func-build-and-deploy"
                    },
                    "annotations": {
                        TEKTON_PRIMARY_KEY_ANNOTATION: str(self.pk),
                    }
                },
                "spec": {
                    "pipelineRef": {
                        "name": "func-build-and-deploy"
                    },
                    # "taskRunSpecs": [{
                    #     "pipelineTaskName": "deploy",
                    #     "taskServiceAccountName": "funckle-func-deploy"
                    # }],
                    "params": [{
                        "name": "gcsPath",
                        "value": "gs://funckle-functions-bucket/" + self.package.name
                    }, {
                        "name": "contextDir",
                        "value": "build"
                    }, {
                        "name": "imageName",
                        "value": self.container_image,
                    }, {
                        "name": "registry",
                        "value": self.container_image_registry,
                    }, {
                        "name": "builderImage",
                        "value": "gcr.io/buildpacks/builder:google-22"
                    }, {
                        "name": "buildEnvs",
                        "value": [
                                "GOOGLE_FUNCTION_TARGET=webhook"
                        ]
                    }, {
                        "name": "function-name",
                        "value": self.function.slug
                        # }, {
                        #     "name": "namespace",
                        #     "value": "default"
                    }],
                    "workspaces": [{
                        "name": "source-workspace",
                        "subPath": "source",
                        "volumeClaimTemplate": {
                                "spec": {
                                    "accessModes": [
                                        "ReadWriteOnce"
                                    ],
                                    "resources": {
                                        "requests": {
                                            "storage": "1Gi"
                                        }
                                    }
                                }
                        }
                    },
                        {
                        "name": "cache-workspace",
                            "subPath": "cache",
                            "volumeClaimTemplate": {
                                "spec": {
                                    "accessModes": [
                                        "ReadWriteOnce"
                                    ],
                                    "resources": {
                                        "requests": {
                                            "storage": "1Gi"
                                        }
                                    }
                                }
                            }
                    }, {
                            "name": "dockerconfig-workspace",
                            "secret": {
                                "secretName": "dockerconfig"
                            }
                    }, {
                            "name": "gcp-credentials",
                            "secret": {
                                "secretName": "gcp-credentials"
                            }
                    }]
                }
            })

    def delete_build_pipeline(self):
        client = Kubernetes.get_client()
        v1 = client.CustomObjectsApi()
        v1.delete_namespaced_custom_object(
            group='tekton.dev',
            version='v1beta1',
            namespace=PIPELINE_RUN_NAMESPACE,
            plural='pipelineruns',
            name=self.pipeline_name,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5)
        )


@receiver(models.signals.pre_save, sender=FunctionVersion)
def rewrite_file_path(sender, instance: FunctionVersion, **kwargs):
    """
    Rewrites the file path to be the same as the version
    """
    if instance.package:
        instance.package.name = instance.package_file_path


@receiver(models.signals.post_delete, sender=FunctionVersion)
def auto_delete_file_on_delete(sender, instance: FunctionVersion, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.package:
        instance.package.delete(save=False)


@receiver(models.signals.post_save, sender=FunctionVersion)
def create_tekton_pipeline(sender, instance: FunctionVersion, created, **kwargs):
    """
    Creates a Tekton Pipeline for the function version
    """
    if created:
        instance.create_build_pipeline()
