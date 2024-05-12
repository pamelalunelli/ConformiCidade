import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import Loader from '../../library/loader/index.js';
import { useToken } from '../../../TokenContext.js';

const MatchingsNotConcluded = () => {
    const { token } = useToken();
    const [historic, setHistoric] = useState([]);
    const [isFetching, setIsFetching] = useState(true);

    const fetchObjetos = async () => {
        try {
            const response = await fetch('/api/userHistory/', {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}` // Adicione o token ao cabeçalho Authorization
                }
            });
            if (!response.ok) {
                throw new Error(`Erro ao buscar objetos: ${response.statusText}`);
            }
            const data = await response.json();
            setHistoric(data);
        } catch (error) {
            toast.error(error.message);
        } finally {
            setIsFetching(false);
        }
    };
    
    useEffect(() => {
        fetchObjetos();
    }, []);

    return (
                <div className="matchings-not-concluded">
            <h2>Matchings não concluídos</h2>
            {isFetching ? (
                <Loader />
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Nome do Arquivo</th>
                            <th>Data</th>
                            <th>Nome do Matching</th>
                        </tr>
                    </thead>
                    <tbody>
                        {historic.map(item => (
                            <tr key={item.id}>
                                <td>{item.nome}</td>
                                <td>{new Date(item.timestamp).toLocaleDateString()}</td>
                                <td>{item.matchingTableName}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default MatchingsNotConcluded;