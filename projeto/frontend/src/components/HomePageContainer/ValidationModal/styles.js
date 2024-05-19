import styled from 'styled-components'
import Modal from '../../library/modals'
import Select from 'react-select'

export const StyledValidationModal = styled(Modal)`
    .modal-content {
        display: flex;
        flex-direction: row;
        width: 100%;
    }

    .form-content {
        flex: 3; /* Ajuste conforme necessário */
        padding: 20px;
    }

    .field-details-panel {
        flex: 1; /* Ajuste conforme necessário */
        padding: 20px;
        border-left: 1px solid #ccc; /* Adicione uma borda para separação */
        background-color: #f9f9f9; /* Cor de fundo para destaque */
    }
`;

StyledValidationModal.Container = styled.div(({theme}) =>`
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: ${theme.spacing.md};
    margin-bottom: ${theme.spacing.lg};
`)

StyledValidationModal.List = styled.ul`
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: ${({theme}) => theme.spacing.md};
`

StyledValidationModal.List.FakeSelect = styled.div(({theme}) =>`
    border-radius: 8px;
    border: 1px solid #B5B5B5;
    opacity: 0.9;
    background: #F3F3F3;

    ${theme.typography.body.base}

    color: #767676;
    padding: ${theme.spacing.sm};
    cursor: not-allowed;
`)

StyledValidationModal.List.Title = styled.h3(({theme}) =>`
    color: #3D3D3D;
    ${theme.typography.body.strong}
    margin: 0 ${theme.spacing.md} 0 0;
    font-size: ${theme.typography.genericFontSize};
`)

StyledValidationModal.Select = styled(Select).attrs({classNamePrefix: 'fieldsSelect'})(({theme}) =>`
    .fieldsSelect{
        &__control{
            border: none;
            border-radius: 8px;
            background: #F3F3F3;
        }
        &__indicator{
            color: #3D3D3D;
            svg{
                width: ${theme.spacing.md};
                height: ${theme.spacing.md};
            }
            &-separator{
                display: none;
            }
        }
        &__value-container{
            ${theme.typography.body.base}
            color: #3D3D3D;
        }
        &__single-value{
            color: #3D3D3D;
            ${theme.typography.body.base}
        } 
        &__menu{
            box-shadow: 0 0 0 0;
            &-list{
                position: absolute;
                width: 100%;
                ${theme.typography.body.base}
                border-radius: 8px;
                color: #3D3D3D;
                border: 1px solid #F1F1F1;
                background: #FBFBFB;
            }
        }
        &__option{
            padding: ${theme.spacing.md};
        }
    }
`)

StyledValidationModal.List.Subtitle = styled.h4(({ theme }) =>`
    color: #3D3D3D;
    ${theme.typography.body.base}
    margin: ${theme.spacing.sm} 0;
    font-size: 1rem;
`)

export const InfoIcon = styled.span`
    cursor: pointer;
    margin-left: 5px;
    // Adicione mais estilos conforme necessário
`;

StyledValidationModal.DisabledField = styled.div`
    border: 1px solid #ccc; /* Adiciona uma borda para indicar que o campo está desativado */
    padding: 5px;
    background-color: #f5f5f5; /* Adiciona um fundo para destacar o campo desativado */
    cursor: not-allowed; /* Altera o cursor para indicar que o campo não é clicável */
`;