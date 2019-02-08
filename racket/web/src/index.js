import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {Provider} from 'react-redux'
import {BrowserRouter, Redirect, Route, Switch} from "react-router-dom";
import {store} from './store'


ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter>
            <Switch>
                <Route exact path='/models' render={props => <App {...props} page={'models'} />}/>
                <Route path='/model/:id' render={props => <App {...props} page={'model'} />}/>
                <Route path='/' >
                    <Redirect to="/models" />
                </Route>
            </Switch>
        </BrowserRouter>
    </Provider>,
    document.getElementById('root'));

serviceWorker.unregister();

