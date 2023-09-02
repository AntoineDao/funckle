import { useCallback, useMemo } from 'react';
import { gql, useMutation, useQuery } from '@apollo/client';
import { notification } from 'antd';

type Props = {
    id: string
}

type EnvironmentVariable = {
    name: string
    value: string
}

type Bot = {
    id: string
    imageUrl: string
    slug: string
    description?: string
    triggers: string[]
    environmentVariables: EnvironmentVariable[]
    secretEnvironmentVariables: EnvironmentVariable[]
    functionVersion: {
        id: string
        version: string
        function: {
            id: string
            slug: string
        }
    }
}


type Stream = {
    id: string,
    speckleId: string,
    name: string,
    imageUrl: string,
    botSet: {
        edges: Array<{
            node: Bot
        }>
    }
}

const GET_STREAM = gql`
query GetStream($id: ID!) {
    stream(id: $id) {
      id
      speckleId
      name
      botSet {
        edges {
          node {
            id
            slug
            description
            triggers
            environmentVariables {
              name
              value
            }
            secretEnvironmentVariables {
              name
              value
            }
            functionVersion {
              id
              version
              function {
                id
                slug
              }
            }
          }
        }
      }
    }
  }
`

type CreateBotProps = {
    functionVersionId: string,
    slug: string,
    description?: string,
    triggers: string[]
    environmentVariables: EnvironmentVariable[]
    secretEnvironmentVariables: EnvironmentVariable[]
}

const CREATE_BOT = gql`
mutation CreateBot(
    $streamId: String!, 
    $functionVersionId: String!,
    $slug:String!,
    $description:String,
    $triggers:[String],
    $environmentVariables: [BotEnvironmentInput],
    $secretEnvironmentVariables: [BotEnvironmentInput]
  ) {
botCreate(
    streamId: $streamId
    functionVersionId:$functionVersionId,
    slug:$slug
    description:$description
    triggers:$triggers
    environmentVariables: $environmentVariables
    secretEnvironmentVariables: $secretEnvironmentVariables
  ) {
    bot {
        id
    }
  }
}
`

const DELETE_BOT = gql`
mutation DeleteBot(
    $id:ID!,
  ) {
    botDelete(
          id:$id
      ) {
        ok
      }
    }
`

export const useStream = ({ id }: Props) => {
    const { loading, error, data, refetch } = useQuery(GET_STREAM, {
        variables: {
            id
        }
    });

    const [BotCreate] = useMutation(CREATE_BOT)
    const [BotDelete] = useMutation(DELETE_BOT)


    const stream = useMemo(() => {
        if (data) {
            return {
                ...data.stream,
                imageUrl: `https://speckle.systems/content/images/2021/02/automation.png`

            } as Stream
        }
        return null
    }, [data])

    const bots = useMemo(() => {
        if (stream) {
            return stream.botSet.edges.map((edge) => ({
                ...edge.node,
                imageUrl: `https://robohash.org/${edge.node.id}`,
            }))
        }
        return []
    }, [stream])

    const createBot = useCallback(async (props: CreateBotProps) => {
        if (stream) {
            // const { functionVersionId, slug, description, triggers,  } = props
            const { errors } = await BotCreate({
                variables: {
                    streamId: stream.speckleId,
                    ...props,
                    // functionVersionId,
                    // slug,
                    // description,
                    // triggers,
                    // environmentVariables,
                }
            })
            if (errors) {
                notification.error({
                    message: 'Error creating bot',
                    description: errors[0].message
                })
            }
            refetch()
        }
    }, [stream, BotCreate, refetch])

    const deleteBot = useCallback(async (id: string) => {
        if (stream) {
            const { errors } = await BotDelete({
                variables: {
                    id
                }
            })
            if (errors) {
                notification.error({
                    message: 'Error deleting bot',
                    description: errors[0].message
                })
            }
            refetch()
        }
    }, [stream, BotDelete, refetch])


    return {
        stream,
        bots,
        loading,
        error,
        createBot,
        deleteBot,
    }
}