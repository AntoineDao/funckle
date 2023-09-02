import { useState, useEffect, useCallback, useMemo } from 'react';
import { gql, useMutation } from '@apollo/client';
import { SPECKLE_SERVER_LINK } from '../context/graphql'

type Props = {
    streamId: string
}

const CREATE_WEBHOOK = gql`
  mutation WebhookCreate($streamId: String!, $url: String!, $triggers: [String]!) {
    webhookCreate(webhook: {streamId: $streamId, url: $url, triggers: $triggers})
  }
`;

export const useCreateWebhook = ({ streamId }: Props) => {

    const [WebhookCreate, { data, loading, error }] = useMutation(CREATE_WEBHOOK, { context: { clientName: SPECKLE_SERVER_LINK } });

    const createWebhook = useCallback((url: string, triggers: string[]) => {
        WebhookCreate({ variables: { streamId, url, triggers } })
    }, [WebhookCreate, streamId])

    const newWebhookId = useMemo(() => {
        if (!data) return null
        return data.webhookCreate
    }, [data])

    return {
        createWebhook,
        newWebhookId,
        loading,
        error
    }
}