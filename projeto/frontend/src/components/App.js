import React from 'react'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import { ThemeProvider } from 'styled-components'
import { TokenProvider } from '../TokenContext.js';
import GlobalStyle from './library/global'
import PageView from './view/PageView'
import { UserProvider } from './Utils/user-utils';
import { theme } from './Utils/theme.utils';

function App() {
    return (
        <>
            <ThemeProvider theme={theme}>
                <GlobalStyle/>
                <ToastContainer position="bottom-left" theme="dark"/>
                <UserProvider>
                    <TokenProvider>
                        <PageView/>
                    </TokenProvider>
                </UserProvider>
            </ThemeProvider>
        </>
    )
}

export default App