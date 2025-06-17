import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider, useLoaderData, BrowserRouter } from 'react-router-dom';
import App from './App';
import StoreContextProvider from './context/storeContext';
import {Provider} from 'react-redux';
import store from './instagram/redux/store';
// import store from './classWork/Foods/redux/store'


const divroot = document.getElementById('root');
const root = ReactDOM.createRoot(divroot);



root.render(
    <div>

    {/* <BrowserRouter>
        <StoreContextProvider>
            <App/>
        </StoreContextProvider>
    </BrowserRouter> */}

    <BrowserRouter>
        <Provider store={store}>
            <App/>
        </Provider>
    </BrowserRouter>

    </div>
);
