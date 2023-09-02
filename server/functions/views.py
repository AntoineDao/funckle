import json
import enum
import logging


from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import FunctionVersion, TEKTON_PRIMARY_KEY_ANNOTATION

logger = logging.getLogger('django')


class TektonEventEnum(enum.Enum):
    PIPELINE_RUN_STARTED = 'dev.tekton.event.pipelinerun.started.v1'
    PIPELINE_RUN_RUNNING = 'dev.tekton.event.pipelinerun.running.v1'
    PIPELINE_RUN_UNKNOWN = 'dev.tekton.event.pipelinerun.unknown.v1'
    PIPELINE_RUN_SUCCEEDED = 'dev.tekton.event.pipelinerun.successful.v1'
    PIPELINE_RUN_FAILED = 'dev.tekton.event.pipelinerun.failed.v1'

    def get_status(self):
        if self == self.PIPELINE_RUN_STARTED:
            return 'STARTED'
        elif self == self.PIPELINE_RUN_RUNNING:
            return 'RUNNING'
        elif self == self.PIPELINE_RUN_UNKNOWN:
            return 'UNKNOWN'
        elif self == self.PIPELINE_RUN_SUCCEEDED:
            return 'SUCCEEDED'
        elif self == self.PIPELINE_RUN_FAILED:
            return 'FAILED'
        else:
            return 'UNKNOWN'


def get_event_type(request: HttpRequest) -> TektonEventEnum:
    header = request.headers.get("Ce-Type", "")
    event_type = TektonEventEnum(header)
    if event_type is None or event_type.value == 'UNKNOWN':
        raise ValueError(f'Invalid event type: {header}')
    return event_type


def get_event_subject(request: HttpRequest) -> str:
    return request.headers.get("Ce-Subject", "")


def get_function_version_pk_from_request(request: HttpRequest) -> str:
    payload = json.loads(request.body)
    return payload.get('pipelineRun', {}).get('metadata', {}).get('annotations', {}).get(TEKTON_PRIMARY_KEY_ANNOTATION, "")


@csrf_exempt
@require_POST
def tekton_webhook(request: HttpRequest):
    try:
        event_type = get_event_type(request)
    except ValueError as e:
        logger.info(e)
        return HttpResponse("Unsupported event type", status=200, content_type="text/plain")

    logger.info(f'Received event type: {event_type.value}')

    subject = get_event_subject(request)

    if not subject:
        logger.info('Missing subject')
        return HttpResponse("Missing subject", status=200, content_type="text/plain")

    logger.info(f'Received subject: {subject}')

    pk_string = get_function_version_pk_from_request(request)

    if pk_string == '':
        logger.info('Missing primary key')
        return HttpResponse("Missing primary key", status=200, content_type="text/plain")

    try:
        pk = int(pk_string)
        function_version = FunctionVersion.objects.get(pk=pk)
    except function_version.DoesNotExist:
        logger.info(f'Invalid primary key: {pk_string}')
        return HttpResponse("Invalid primary key", status=200, content_type="text/plain")

    logger.info(
        f'Setting status to {event_type.get_status()} for function version {function_version.pk}')

    function_version.status = event_type.get_status()

    if event_type in [TektonEventEnum.PIPELINE_RUN_SUCCEEDED, TektonEventEnum.PIPELINE_RUN_FAILED]:
        function_version.save_build_logs()
        function_version.delete_build_pipeline()

    function_version.save()

    return HttpResponse("Message received okay.", content_type="text/plain")
