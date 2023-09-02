import { useCallback, useMemo } from 'react';
import { gql, useMutation } from '@apollo/client';
import { SPECKLE_SERVER_LINK } from '../context/graphql'

type Props = {
}

const CREATE_API_TOKEN = gql`
  mutation ApiTokenCreate($name: String!, $scopes: [String]!) {
    apiTokenCreate(token:{name: $name, scopes: $scopes})
}
`;

export const useCreateApiToken = ({ }: Props) => {

    const [ApiTokenCreate, { data, loading, error }] = useMutation(CREATE_API_TOKEN, { context: { clientName: SPECKLE_SERVER_LINK } });

    const createApiToken = useCallback((name: string, scopes: string[]) => {
        ApiTokenCreate({ variables: { name, scopes } })
    }, [ApiTokenCreate])

    const newApiToken = useMemo(() => {
        if (!data) return ""
        return data.apiTokenCreate as string
    }, [data])

    return {
        createApiToken,
        newApiToken,
        loading,
        error
    }
}