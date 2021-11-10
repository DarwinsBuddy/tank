import { FunctionalComponent } from 'preact';
import { Route, Router } from 'preact-router';

import Home from './routes/home';
import NotFoundPage from './routes/notfound';
import { jsx } from '@emotion/react';
import Header from './components/header';
import { ConfigContext, config, SocketContext, socket } from './components/context/global-context';

const App: FunctionalComponent = () => {
    return (
        <div id="preact_root">
            <ConfigContext.Provider value={config}>
                <SocketContext.Provider value={socket}>
                    <Header />
                    <Router>
                        <Route path="/" component={Home} />
                        <NotFoundPage default />
                    </Router>
                </SocketContext.Provider>
            </ConfigContext.Provider>
        </div>
    );
};

export default App;
