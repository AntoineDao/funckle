import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphql_relay.node.node import from_global_id
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from slugify import slugify

from functions.models import Function, FunctionVersion

from .utils import get_auth_user


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )
        include = ('id', 'username', 'first_name', 'last_name')
        exclude = ('password', 'is_superuser', 'is_staff', 'is_active')


class FunctionNode(DjangoObjectType):
    class Meta:
        model = Function
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'slug': ['exact', 'icontains', 'istartswith'],
            'description': ['istartswith', 'icontains'],
        }
        interfaces = (relay.Node, )
        exclude = ()


class FunctionVersionNode(DjangoObjectType):
    class Meta:
        model = FunctionVersion
        interfaces = (relay.Node, )
        exclude = ('build_logs',)

    build_logs = graphene.String(
        resolver=lambda instance, resolve_obj: instance.build_logs_text)


class CreateFunction(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        readme = graphene.String()
        source_location = graphene.String()

    function = graphene.Field(FunctionNode)

    def mutate(self, info, name, description, readme, source_location):
        user = get_auth_user(info)
        function = Function(
            owner=user,
            name=name,
            slug=slugify(name),
            description=description,
            readme=readme,
            source_location=source_location,
        )

        function.save()

        return CreateFunction(function=function)


class UpdateFunction(graphene.Mutation):
    class Arguments:
        slug = graphene.String()
        description = graphene.String()
        readme = graphene.String()
        source_location = graphene.String()

    function = graphene.Field(FunctionNode)

    def mutate(self, info, slug, description, readme, source_location):
        user = get_auth_user(info)
        function = Function.objects.get(owner=user, slug=slug)

        if function.DoesNotExist:
            raise GraphQLError(
                f'Function with slug does not exist for owner: {user.username}/{slug}')

        if function.owner != user:
            raise GraphQLError(f'Cannot update someone else\'s function')

        function.description = description
        function.readme = readme
        function.source_location = source_location
        function.save()

        return CreateFunction(function=function)


class DeleteFunction(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    def mutate(self, info, id):
        user = get_auth_user(info)
        if user.is_anonymous:
            raise GraphQLError(f'User must be authenticated')

        _, pk = from_global_id(id)
        function = Function.objects.get(pk=pk)

        if function.DoesNotExist:
            return DeleteFunction(success=True)

        if function.owner != user:
            raise GraphQLError(f'Cannot delete someone else\'s function')

        function.delete()

        return DeleteFunction(success=True)


class FunctionVersionUpload(graphene.Mutation):
    class Arguments:
        # function_slug = graphene.String(required=True)
        name = graphene.String()
        description = graphene.String()
        readme = graphene.String()
        source_location = graphene.String()
        version = graphene.String(required=True)
        file = Upload(required=True)

    function_version = graphene.Field(FunctionVersionNode)

    def mutate(self, info, file, name, description, readme, source_location, version):
        user = get_auth_user(info)
        slug = slugify(name)

        function, _ = Function.objects.get_or_create(owner=user, slug=slug)

        function.name = name
        function.description = description
        function.readme = readme
        function.source_location = source_location
        function.save()

        # Maybe add an assertion for the type of 'file' being a file
        function_version = FunctionVersion(
            function=function,
            version=version,
            package=file
        )

        function_version.save()
        return FunctionVersionUpload(function_version=function_version)
