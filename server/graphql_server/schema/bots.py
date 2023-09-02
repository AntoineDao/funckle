import uuid
import graphene

from graphene import relay
from graphene_django import DjangoObjectType
from graphql_relay.node.node import from_global_id
from graphql import GraphQLError
from slugify import slugify

from functions.models import FunctionVersion
from bots.models import Stream, Bot
from .utils import get_auth_user, get_speckle_client


class StreamNode(DjangoObjectType):
    class Meta:
        model = Stream
        interfaces = (relay.Node, )
        filter_fields = {
            'speckle_id': ['exact'],
        }


class BotEnvironmentVariables(graphene.ObjectType):
    name = graphene.String(required=True)
    value = graphene.String(required=True)


class BotNode(DjangoObjectType):
    class Meta:
        model = Bot
        interfaces = (relay.Node,)
        exclude = ()

    triggers = graphene.List(graphene.String)
    environmentVariables = graphene.List(
        BotEnvironmentVariables,
        resolver=lambda instance, resolve_obj: [
            {'name': key, 'value': value} for key, value in instance.environment_variables.items()]
    )
    secretEnvironmentVariables = graphene.List(
        BotEnvironmentVariables,
        resolver=lambda instance, resolve_obj: [
            {'name': key, 'value': value} for key, value in instance.environment_secrets.items()]
    )


class BotEnvironmentInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    value = graphene.String(required=True)


class CreateBot(graphene.Mutation):
    class Arguments:
        streamId = graphene.String(required=True)
        slug = graphene.String(required=True)
        functionVersionId = graphene.String(required=True)
        description = graphene.String(required=False)
        triggers = graphene.List(graphene.String)
        environmentVariables = graphene.List(BotEnvironmentInput)
        secretEnvironmentVariables = graphene.List(BotEnvironmentInput)

    # The class attributes define the response of the mutation
    bot = graphene.Field(BotNode)

    @classmethod
    def mutate(cls, root, info, streamId,  slug, functionVersionId, description, triggers, environmentVariables, secretEnvironmentVariables):
        user = get_auth_user(info)
        if user.is_anonymous:
            raise GraphQLError(f'User must be authenticated')

        _, pk = from_global_id(functionVersionId)
        try:
            fv = FunctionVersion.objects.get(pk=pk)
        except FunctionVersion.DoesNotExist:
            raise GraphQLError(
                f'Function version with ID does not exist: {functionVersionId}')

        try:
            stream = Stream.objects.get(speckle_id=streamId)
        except Stream.DoesNotExist:
            raise GraphQLError(f'Stream with ID does not exist: {streamId}')

        speckle = get_speckle_client(info)
        secret = uuid.uuid4().hex

        slug = slugify(slug)

        try:
            webhook_id = Bot.create_webhook(
                client=speckle, stream_id=stream.speckle_id,
                url=Bot.generate_url(slug, user.username),
                triggers=triggers, secret=secret,
                description=f'Funckle Bot {slug}'
            )
        except Exception as err:
            raise GraphQLError(f'Failed to create webhook: {err}')

        environment_variable = {}
        if environmentVariables is not None:
            for env in environmentVariables:
                environment_variable[env.name] = env.value

        environment_secret = {
            'FUNCKLE_WEBHOOK_SECRET': secret,
        }
        if secretEnvironmentVariables is not None:
            for env in secretEnvironmentVariables:
                environment_secret[env.name] = env.value

        bot = Bot.objects.create(
            owner=info.context.user,
            slug=slug,
            description=description,
            stream=stream,
            webhook_id=webhook_id,
            function_version=fv,
            triggers=triggers,
            environment_variables=environment_variable,
            environment_secrets=environment_secret,
        )
        return CreateBot(bot=bot)


class UpdateBot(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        functionVersionId = graphene.String(required=True)
        description = graphene.String()
        triggers = graphene.List(graphene.String)
        environmentVariables = graphene.List(BotEnvironmentInput)
        secretEnvironmentVariables = graphene.List(BotEnvironmentInput)

    # The class attributes define the response of the mutation
    bot = graphene.Field(BotNode)

    @classmethod
    def mutate(cls, root, info, id, functionVersionId, description, triggers, environmentVariables, secretEnvironmentVariables):
        user = get_auth_user(info)
        if user.is_anonymous:
            raise GraphQLError(f'User must be authenticated')

        _, pk = from_global_id(id)
        try:
            bot = Bot.objects.get(pk=pk)
        except Bot.DoesNotExist:
            raise GraphQLError(f"Bot with ID does not exist: {id}")

        if bot.owner != user:
            raise GraphQLError(f'Cannot update someone else\'s bot')

        _, pk = from_global_id(functionVersionId)
        try:
            fv = FunctionVersion.objects.get(pk=pk)
        except FunctionVersion.DoesNotExist:
            raise GraphQLError(
                f'Function version with ID does not exist: {functionVersionId}')

        speckle = get_speckle_client(info)
        secret = uuid.uuid4().hex

        try:
            Bot.update_webhook(
                client=speckle,
                stream_id=bot.stream.speckle_id,
                webhook_id=bot.webhook_id,
                # url=f'https://{slug}.{info.context.user.username}.apps.staging.pollination.cloud',
                url=Bot.generate_url(bot.slug, bot.owner.username),
                triggers=triggers,
                secret=secret,
            )
        except Exception as err:
            raise GraphQLError(f'Failed to update the webhook: {err}')

        environment_variable = {}
        for env in environmentVariables:
            environment_variable[env.name] = env.value

        environment_secret = {}
        for env in secretEnvironmentVariables:
            environment_secret[env.name] = env.value

        environment_secret['FUNCKLE_WEBHOOK_SECRET'] = secret

        bot.description = description
        bot.function_version = fv
        bot.environment_variables = environment_variable
        bot.environment_secrets = environment_secret

        bot.save()

        return UpdateBot(bot=bot)


class DeleteBot(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        user = get_auth_user(info)
        if user.is_anonymous:
            raise GraphQLError(f'User must be authenticated')

        _, pk = from_global_id(id)
        try:
            bot = Bot.objects.get(pk=pk)
        except Bot.DoesNotExist:
            return DeleteBot(ok=True)

        if bot.owner != user:
            raise GraphQLError(f'Cannot delete someone else\'s bot')

        speckle = get_speckle_client(info)
        Bot.delete_webhook(
            client=speckle, stream_id=bot.stream.speckle_id, webhook_id=bot.webhook_id
        )
        bot.delete()
        return DeleteBot(ok=True)
