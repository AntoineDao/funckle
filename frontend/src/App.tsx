import React from 'react';
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route,
  Link,
} from "react-router-dom";
import { Result, Button } from 'antd';

import { AuthProvider } from './context/auth'
import { GraphqlProvider } from './context/graphql';

import Root from './components/templates/Root'
import AuthCallback from './components/atoms/AuthCallback';
import { UserProvider } from './context/user';
import StreamWrapper from './components/templates/StreamWrapper';
import StreamList from './components/molecules/StreamList';
import Stream from './components/organisms/Stream'
import Function from './components/organisms/Function'
import FunctionWrapper from './components/templates/FunctionWrapper';
import FunctionList from './components/molecules/FunctionList';
import CreateFunction from './components/pages/CreateFunction';
import Index from './components/templates/Index';

const App = () => {
  return (
    <AuthProvider>
      <GraphqlProvider>
        <UserProvider>
          <RouterProvider router={createBrowserRouter(
            createRoutesFromElements(
              <Route
                path=""
                element={<Root />}
                errorElement={(
                  <Root>
                    <Result
                      status="404"
                      title="404"
                      subTitle="Sorry, the page you visited does not exist."
                      extra={<Link to="/"><Button type="primary">Back Home</Button></Link>}
                    />
                  </Root>
                )}
              >
                <Route index element={<Index />} />
                <Route path="auth" element={<AuthCallback />} />
                <Route path="functions" element={<FunctionWrapper />}>
                  <Route index element={<FunctionList />} />
                  <Route path="new" element={<CreateFunction />} />
                  <Route path=":functionId" element={<Function />}>
                    <Route path=":versionId" />
                  </Route>
                </Route>
                <Route path="streams" element={<StreamWrapper />}>
                  <Route index element={<StreamList />} />
                  <Route path=":streamId" element={<Stream />}>
                    <Route path="new" />
                    <Route path=":botId" />
                  </Route>
                </Route>
              </Route>

            )
          )} />
        </UserProvider>
      </GraphqlProvider>
    </AuthProvider>
  );
}

export default App;
