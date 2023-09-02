import uuid
import graphene
from graphene import relay, ObjectType
from graphql_relay.node.node import from_global_id
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from bots.models import Stream, Bot

from .functions import FunctionNode, CreateFunction, UpdateFunction, DeleteFunction, FunctionVersionUpload
from .bots import StreamNode, BotNode, CreateBot, UpdateBot, DeleteBot
from .utils import get_speckle_client


class Query(ObjectType):
    functions = DjangoFilterConnectionField(FunctionNode)
    function = relay.Node.Field(FunctionNode)

    streams = DjangoFilterConnectionField(StreamNode)
    stream = relay.Node.Field(StreamNode)
    bot = relay.Node.Field(BotNode)

    bot_logs = graphene.List(
        graphene.String, botId=graphene.ID(required=True))

    def resolve_streams(self, info):
        speckle = get_speckle_client(info)
        streams = speckle.stream.list(stream_limit=50)
        stream_objects = [
            Stream(
                speckle_id=stream.id,
                name=stream.name,
                # description=stream.description,
            ) for stream in streams if stream.role == 'stream:owner'
        ]

        Stream.objects.bulk_create(stream_objects, ignore_conflicts=True)
        return Stream.objects.filter(speckle_id__in=[stream.speckle_id for stream in stream_objects])

    def resolve_bot_logs(self, info, botId):
        _, pk = from_global_id(botId)
        try:
            bot = Bot.objects.get(pk=pk)
        except Bot.DoesNotExist:
            raise GraphQLError('Bot not found')

        return bot.get_logs()


class Mutation(graphene.ObjectType):
    bot_create = CreateBot.Field()
    bot_update = UpdateBot.Field()
    bot_delete = DeleteBot.Field()
    # function_create = CreateFunction.Field()
    # update_function = UpdateFunction.Field()
    delete_function = DeleteFunction.Field()
    upload_package = FunctionVersionUpload.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
