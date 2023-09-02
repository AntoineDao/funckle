import React, { createContext, useContext, useMemo, useState } from 'react'

import { ApolloClient, createHttpLink, InMemoryCache, ApolloProvider, ApolloLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

import { useAuth } from './auth'



const SPECKLE_SERVER_URL = 'https://speckle.xyz'
// const FUNCKLE_SERVER_URL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8000'
const FUNCKLE_SERVER_URL = 'https://app.funckle.nerd-extraordinaire.com'

export const SPECKLE_SERVER_LINK = 'speckleServerLink'

export const GraphqlProvider = ({ children }: any) => {

    const { token } = useAuth()

    const speckleServerLink = createHttpLink({
        uri: `${SPECKLE_SERVER_URL}/graphql`,
    })

    const funckleServerLink = createHttpLink({
        uri: `${FUNCKLE_SERVER_URL}/graphql`,
    })

    const authLink = useMemo(() => setContext((_, { headers }) => {
        // get the authentication token from local storage if it exists
        // return the headers to the context so httpLink can read them
        return {
            headers: {
                ...headers,
                authorization: token ? `Bearer ${token}` : "",
            }
        }
    }), [token])

    const client = useMemo(() => new ApolloClient({
        link: ApolloLink.split(
            operation => operation.getContext().clientName === SPECKLE_SERVER_LINK, // Routes the query to the Speckle client
            authLink.concat(speckleServerLink), //if above 
            authLink.concat(funckleServerLink) //if not above
        ),
        cache: new InMemoryCache()
    }), [authLink, speckleServerLink, funckleServerLink])

    return (
        <ApolloProvider client={client}>
            {children}
        </ApolloProvider>
    )
}
