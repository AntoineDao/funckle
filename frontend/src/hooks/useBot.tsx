import { useCallback, useMemo } from 'react';
import { gql, useMutation, useQuery } from '@apollo/client';
import { useNavigate } from "react-router-dom";
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

const GET_BOT = gql`
query GetBot($id: ID!) {
    bot(id: $id) {
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
`

type UpdateBotProps = {
  functionVersionId: string,
  // slug: string,
  description: string | undefined,
  triggers: string[]
  environmentVariables: EnvironmentVariable[]
  secretEnvironmentVariables: EnvironmentVariable[]

}

const UPDATE_BOT = gql`
mutation UpdateBot(
    $id: ID!, 
    $functionVersionId: String!, 
    $description: String, 
    $triggers: [String],
    $environmentVariables: [BotEnvironmentInput],
    $secretEnvironmentVariables: [BotEnvironmentInput]
  ) {
    botUpdate(
      id: $id
      functionVersionId:$functionVersionId,
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

const BOT_LOGS = gql`
query BotLogs($id:ID!) {
  botLogs(botId:$id) 
}
`

export const useBot = ({ id }: Props) => {
  const { loading, error, data, refetch } = useQuery(GET_BOT, {
    variables: {
      id
    },
    pollInterval: 10000
  });

  const { data: logsData, error: logsError, refetch: logsRefetch } = useQuery(BOT_LOGS, {
    variables: {
      id
    },
    pollInterval: 10000
  });

  const navigate = useNavigate();

  const [botUpdate] = useMutation(UPDATE_BOT);
  const [BotDelete] = useMutation(DELETE_BOT)


  const bot = useMemo(() => {
    if (data) {
      return {
        ...data.bot,
        imageUrl: `https://robohash.org/${data.id}`

      } as Bot
    }
    return null
  }, [data])

  const updateBot = useCallback(async (update: UpdateBotProps) => {
    if (bot) {
      const { errors } = await botUpdate({
        variables: {
          id: bot.id,
          functionVersionId: update.functionVersionId,
          description: update.description,
          triggers: update.triggers,
          environmentVariables: update.environmentVariables.map((env) => ({
            name: env.name,
            value: env.value
          })),
          secretEnvironmentVariables: update.secretEnvironmentVariables.map((env) => ({
            name: env.name,
            value: env.value
          })),
        }
      })
      if (errors) {
        notification.error({
          message: 'Error updating bot',
          description: errors[0].message
        })
      }
      refetch()
    }
  }, [bot, botUpdate, refetch])



  const deleteBot = useCallback(async (id: string) => {
    if (bot) {
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
      navigate(`/streams`)
    }
  }, [bot, BotDelete, navigate])


  const botLogs = useMemo(() => {
    if (logsData) {
      return logsData.botLogs as string[]
    }
    return ["No logs found"]
  }, [logsData])

  return {
    bot,
    botLogs,
    updateBot,
    deleteBot,
    loading,
    error,
    refetch,
  }
}