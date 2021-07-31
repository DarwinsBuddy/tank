import { FunctionalComponent, h } from 'preact';
import { Route, Router } from 'preact-router';

import Home from '../routes/home';
//import Profile from '../routes/profile';
import NotFoundPage from '../routes/notfound';
import Header from './header';
import { ConfigContext, config, SocketContext, socket } from './context/global-context';

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

// <Route path="/profile/" component={Profile} user="me" />
// <Route path="/profile/:user" component={Profile} />

export default App;
