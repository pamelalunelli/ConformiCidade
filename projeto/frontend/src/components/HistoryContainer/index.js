import React, { useEffect, useState } from 'react'
import { toast } from 'react-toastify'

import { Pen, TrashAlt, Download } from '../library/icons'
import Modal from '../library/modals'
import { PrimaryButton, SecondaryButton } from '../library/buttons'
import Loader from '../library/loader'

import { StyledHistoryContainer } from './styles'
import { useToken } from '../../TokenContext.js';

const HistoryContainer = ({
}) => {
    const { token } = useToken()
    const [historic, setHistoric] = useState()
    const [isFetching, setIsFetching] = useState(true)

    const [modalIsOpen, setIsOpen] = useState(false)
    const [modalData, setModalData] = useState('')

    const [editingNameId, setEditingNameId] = useState(null)
    const [newName, setNewName] = useState(null)
    
    const openModal = (data) => {
        setIsOpen(true)
        setModalData(data)
    }
    const closeModal = () => {
        setModalData('')
        setIsOpen(false)
    }

    const fetchObjetos = async () => {
        try {
            setIsFetching(true)
            const response = await fetch('/api/userHistory/', {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}` // Adicione o token ao cabeçalho Authorization
                }
            });
            const data = await response.json()
            setHistoric(data)
        } catch (error) {
            toast.error('Erro ao buscar objetos:', error)
        } finally {
            setIsFetching(false)
        }
      }

    useEffect(() => {
      fetchObjetos()
    }, [])

    const handleDelete = (id) => {
        fetch(`/api/userHistory/${id}/delete/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => response.json())
          .then(data => {
            toast.success('Arquivo excluído com sucesso')
            closeModal()
            fetchObjetos()
          })
          .catch(error => {
            toast.error('Erro ao excluir')
          })
    }

    const handleEdit = (id, newName) => {
        fetch(`/api/userHistory/${id}/edit/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nome: newName }),
        })
        .then(response => response.json())
        .then(data => {
            toast.success('Arquivo renomeado com sucesso')
            setEditingNameId(null)
            fetchObjetos()
        })
        .catch(error => {
            toast.error('Erro ao editar')
        })
    }

    const handleDownload = (id) => {
        fetch(`/api/download_pdf/${id}/`, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`
            }
        }).then(response => {
            if (response.ok) {
                response.blob().then(blob => {
                    const url = window.URL.createObjectURL(new Blob([blob]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', `file.pdf`);
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });
            } else {
                toast.error('Erro ao fazer o download do PDF');
            }
        }).catch(error => {
            toast.error('Erro ao fazer o download do PDF:', error);
        });
    }

    return (
        <>
            <StyledHistoryContainer>
                <StyledHistoryContainer.Title>
                    Histórico
                </StyledHistoryContainer.Title>
                {isFetching ? <Loader/> : (
                    <StyledHistoryContainer.Table>
                        <thead>
                            <tr>
                                <th>
                                    Arquivo
                                </th>
                                <th>
                                    Data de envio
                                </th>
                                <th>
                                    Ações
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {!!historic && historic.length > 0 ? (
                                historic.map(item => ( console.log(item),
                                    <tr key={item.id}>
                                        <td>
                                            {editingNameId === item.id ? (
                                                <StyledHistoryContainer.Table.Editing>
                                                    <StyledHistoryContainer.RenameInput defaultValue={item.nome} onChange={(e) => setNewName(e.target.value)}/>
                                                    <div>
                                                        <PrimaryButton disabled={newName === '' || !newName} size='SMALL' onClick={() => handleEdit(item.id, newName)}>
                                                            Confirmar
                                                        </PrimaryButton>
                                                        <SecondaryButton size='SMALL' onClick={() => setEditingNameId(null)}>
                                                            Cancelar
                                                        </SecondaryButton>
                                                    </div>
                                                </StyledHistoryContainer.Table.Editing>
                                            ) : (
                                                <StyledHistoryContainer.FileName>{item.nome}</StyledHistoryContainer.FileName>
                                            )} 
                                        </td>
                                        <td>
                                        {new Date(item.timestamp).toLocaleString('pt-BR', { 
                                            day: '2-digit', 
                                            month: '2-digit', 
                                            year: 'numeric', 
                                            hour: '2-digit', 
                                            minute: '2-digit', 
                                            second: '2-digit', 
                                            hour12: false 
                                        })}
                                        </td>
                                        <td>
                                            <StyledHistoryContainer.Actions>
                                                <StyledHistoryContainer.RenameButton onClick={() => setEditingNameId(item.id)}>
                                                    <Pen/> <span>Renomear</span>
                                                </StyledHistoryContainer.RenameButton>
                                                <StyledHistoryContainer.RemoveButton onClick={() => openModal(item)}>
                                                    <TrashAlt/> <span>Excluir</span>
                                                </StyledHistoryContainer.RemoveButton>
                                                <StyledHistoryContainer.DownloadButton onClick={() => handleDownload(item.id)}>
                                                    <Download /> <span>Baixar</span>
                                                </StyledHistoryContainer.DownloadButton>
                                            </StyledHistoryContainer.Actions>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td rowSpan={3}>
                                        Nenhum dado encontrado
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </StyledHistoryContainer.Table>
                )}
            </StyledHistoryContainer>
            <Modal primaryButtonLabel={'Confirmar'}
                   btnType={'submit'}
                   isOpen={modalIsOpen}
                   onClose={closeModal}
                   handleClick={() => handleDelete(modalData.id)}>
                Tem certeza que deseja remover o arquivo <strong>{modalData.nome}</strong> do seu histórico?
            </Modal>
        </>
    )
}

export default HistoryContainer