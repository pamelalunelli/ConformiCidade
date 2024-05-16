import styled from 'styled-components'

export const StyledHelpContainer = styled.section`
`

StyledHelpContainer.Title = styled.h1`
    margin: 0;
    ${({theme}) => theme.typography.title.xl};
`
StyledHelpContainer.IntermediateTitle = styled.h2`
    margin: 0;
    ${({theme}) => theme.typography.title.lg}; /* Estilo intermediário */
`
StyledHelpContainer.Paragraph = styled.p(({theme}) =>`
    margin-top: ${theme.spacing.lg};
    ${theme.typography.body.base};
`)