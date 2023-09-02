import { useMemo } from 'react';
import { gql, useQuery } from '@apollo/client';

type Props = {
    id: string
}

export type FunctionVersion = {
    id: string
    version: string
    status: string
    buildLogs: string
    createdAt: string
    updatedAt: string
}

type Owner = {
    specklId: string
    name: string
    avatar: string
}

export type Function = {
    id: string
    slug: string
    name: string
    description?: string
    readme?: string
    owner: Owner
    functionversionSet: {
        edges: Array<{
            node: FunctionVersion
        }>
    }
}

const GET_FUNCTION = gql`
query GetFunction($id:ID!){
    function(id:$id) {
      id
      owner {
        specklId: username
        name: firstName
        avatar: lastName
      }
      slug
      name
      description
      readme
      functionversionSet {
        edges{
          node {
            id
            version
            status
            buildLogs
            createdAt
            updatedAt
          }
        }
      }
    }
  }
`


export const useFunction = ({ id }: Props) => {
    const { loading, error, data, refetch } = useQuery(GET_FUNCTION, {
        variables: {
            id
        },
        pollInterval: 10000,
    });

    const func = useMemo(() => {
        if (data) {
            return {
                ...data.function,
                imageUrl: `https://robohash.org/${id}?set=set4`
            } as Function
        }
        return null
    }, [data, id])

    const functionVersions = useMemo(() => {
        if (func) {
            return func.functionversionSet.edges.map((edge) => ({
                ...edge.node,
            })).sort((a, b) => {
                return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
            })
        }
        return []
    }, [func])



    return {
        func,
        functionVersions,
        loading,
        error,
    }
}