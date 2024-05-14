import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import Loader from '../../library/loader/index.js';
import { useToken } from '../../../TokenContext.js';
import { StyledMatchingsNotConcludedTable } from './styles.js';

const MatchingsNotConcluded = () => {
    const { token } = useToken();
    const [historic, setHistoric] = useState([]);
    const [isFetching, setIsFetching] = useState(true);

    useEffect(() => {
        fetchObjetos();
    }, []);

    const fetchObjetos = async () => {
        try {
            const response = await fetch('/api/unfinished_matching/', {
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

    const handleRowClick = async (iduser, id) => {
        try {
            const response = await fetch('/api/identifying_autosaved_fields/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    iduser,
                    id
                })
            });
            if (!response.ok) {
                throw new Error(`Erro ao recuperar campos autosaved: ${response.statusText}`);
            }
            toast.success('Campos autosaved recuperados com sucesso!');
        } catch (error) {
            toast.error(error.message);
        }
    };

    return (
        <div className="matchings-not-concluded">
            <h2>Matchings não concluídos</h2>
            {isFetching ? (
                <Loader />
            ) : (
                <StyledMatchingsNotConcludedTable> {/* Aplica os estilos à tabela */}
                    <thead>
                        <tr>
                            <th>Nome do Arquivo</th>
                            <th>Data</th>
                            <th>Nome do Matching</th>
                        </tr>
                    </thead>
                    <tbody>
                        {historic.map(item => (
                            <tr key={item.id} onClick={() => handleRowClick(item.iduser, item.id)}>
                                <td>{item.nome}</td>
                                <td>{new Date(item.timestamp).toLocaleDateString()}</td>
                                <td>{item.matchingTableName}</td>
                            </tr>
                        ))}
                    </tbody>
                </StyledMatchingsNotConcludedTable>
            )}
        </div>
    );
};

export default MatchingsNotConcluded;