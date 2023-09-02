import { useMemo, useState } from 'react';
import { gql, useQuery } from '@apollo/client';

type Props = {
}

export type Function = {
  id: string,
  slug: string,
  name: string,
  imageUrl: string,
  description: string,
  owner: {
    id: string,
    speckleId: string,
    name?: string,
    avatar: string
  },
  functionversionSet: {
    edges: Array<{
      node: {
        id: string,
        version: string,
        package: string,
        status: string,
        createdAt: string,
        updatedAt: string,
      }
    }>
  }
}

const GET_FUNCTIONS = gql`
query Functions($slug: String){
    functions(slug_Icontains: $slug) {
      edges {
        node {
          id
          name
          slug
          description
          owner{
            id
            speckleId: username
            name:firstName
            avatar: lastName
          }
          functionversionSet {
            edges {
              node {
                id
                version
                package
                status
                createdAt
                updatedAt
              }
            }
          }   
        }
      }
    }
  }
`;

type FunctionQuery = {
  slug?: string,
}

export const useFunctions = ({ }: Props) => {
  const [query, setQuery] = useState<FunctionQuery>()

  const { loading, error, data } = useQuery(GET_FUNCTIONS, {
    variables: query
  });


  const functions = useMemo(() => {
    if (data) {
      return data.functions.edges.map((edge: any) => ({
        ...edge.node,
        imageUrl: `https://robohash.org/${edge.node.id}?set=set4`
      })) as Function[]
    }
    return []
  }, [data])

  return {
    functions,
    loading,
    error,
    setQuery,
  }
}