import React, { createContext, useContext, useState } from 'react';

// Criando o contexto do token
const TokenContext = createContext();

// Hook para consumir o contexto do token
export const useToken = () => useContext(TokenContext);

// Provedor do contexto do token
export const TokenProvider = ({ children }) => {
    const [token, setToken] = useState('');

    return (
        <TokenContext.Provider value={{ token, setToken }}>
            {children}
        </TokenContext.Provider>
    );
};