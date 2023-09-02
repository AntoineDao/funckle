import { useCallback, useMemo } from 'react';
import { gql, useQuery } from '@apollo/client';

type Props = {}

type Stream = {
  id: string,
  speckleId: string,
  name: string,
  imageUrl: string,
  botSet: {
    edges: Array<{
      node: {
        id: string,
        webhookId: string,
        functionVersion: {
          version: string,
          function: {
            slug: string
          }
        }
      }
    }>
  }
}

const GET_STREAMS = gql`
query GetStreams {
    streams{
      edges {
        node {
          id
          speckleId
          name
          botSet{
            edges{
              node {
                id
                webhookId
                functionVersion {
                  version
                  function {
                    slug
                  }
                }
              }
            }
          }
        }
      }
    }
}
`;


export const useStreams = ({ }: Props) => {
  const { loading, error, data } = useQuery(GET_STREAMS);

  const streams = useMemo(() => {
    if (data) {
      return data.streams.edges.map((edge: any) => ({
        ...edge.node,
        imageUrl: `https://robohash.org/${edge.node.speckleId}?set=set4`
      })) as Stream[]
    }
    return []
  }, [data])

  return {
    streams,
    loading,
    error
  }
}