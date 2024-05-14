import styled from 'styled-components';


export const StyledMatchingsNotConcludedTable = styled.table(({ theme }) => `
    width: 100%;
    border-radius: 8px;
    border-collapse: collapse;
    overflow: hidden;

    thead {
        background: #F3F3F3;
        color: #3D3D3D;
    }

    th {
        ${theme.typography.body.strong};
    }

    td {
        ${theme.typography.body.base};
    }

    th, td {
        padding: ${theme.spacing.sm};
        text-align: left;
        text-wrap: nowrap;

        &:first-of-type {
            width: 60%;
            padding-left: ${theme.spacing.md};
        }

        &:last-of-type {
            padding-right: ${theme.spacing.md};
        }
    }

    tr {
        border-bottom: 1px solid #B5B5B5;
        cursor: pointer; /* Adiciona cursor de apontar para indicar clicabilidade */
    }

    tbody {
        color: #767676;
    }
`);
