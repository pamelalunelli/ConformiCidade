import React from 'react'

import { StyledHelpContainer } from './styles'

const HelpContainer = () => (
    <StyledHelpContainer>
        <div>
            <StyledHelpContainer.Title>Ajuda e informações</StyledHelpContainer.Title>
            <StyledHelpContainer.IntermediateTitle>
            Sobre a Aplicação
            </StyledHelpContainer.IntermediateTitle>
            <StyledHelpContainer.Paragraph>
            Esta aplicação foi desenvolvida como parte do Trabalho de Conclusão de Curso (TCC) de Pâmela Andressa Lunelli, graduanda em Tecnologias da Informação e Comunicação (TIC) da Universidade Federal de Santa Catarina, com orientação da Profª Drª Andrea Sabedra Bordin (Universidade Federal de Santa Catarina) e co-orientação da Profª Drª Suzana Daniela Rocha Santos e Silva (Universidade Federal da Bahia).
            O desenvolvimento visa faciliar a validação de modelos de dados de sistemas tributários municipais ao momento de uma potencial integração com cadastros territoriais multifinalitários. 
            </StyledHelpContainer.Paragraph>

            <StyledHelpContainer.IntermediateTitle>
            Como Funciona
            </StyledHelpContainer.IntermediateTitle>
            <StyledHelpContainer.Paragraph>
            Validação de Modelos de Entrada: A aplicação permite a inserção de modelos de entrada e verifica a conformidade desse modelo em relação aos modelo de referência proposto e implementado na ferramenta.
            Geração de Relatórios de Conformidade: Após a validação, a aplicação compara os modelos de entrada com o modelo de referência, identificando discrepâncias e inconsistências, gerando relatórios destacando os campos de conformidade ou desconformidade, apontando percentuais de aderência ao modelo de referência.
            </StyledHelpContainer.Paragraph>

            <StyledHelpContainer.IntermediateTitle>
            Utilizando a Aplicação
            </StyledHelpContainer.IntermediateTitle>
            <StyledHelpContainer.Paragraph>
            Carregando os Modelos de Entrada: é possível carregar os modelos de entrada desde que certificando-se de que os formatos de arquivo são compatíveis (*.csv ou *.txt).
            Iniciando a Validade: Após carregar o modelo de entrada, inicia o processo de validação e uma janela de correspondência entre campos será carregada. A aplicação processa os dados e fornece feedback instantâneo sobre sua conformidade com os padrões estabelecidos.
            Revisão dos Relatórios: após a validação, os relatórios estarão disponíveis na seção de 'Histórico' e os matchings ainda não finalizados são apresentados na tela inicial e podem ser concluídos a qualquer momento.
            </StyledHelpContainer.Paragraph>

            <StyledHelpContainer.IntermediateTitle>
            Suporte
            </StyledHelpContainer.IntermediateTitle>
            <StyledHelpContainer.Paragraph>
            Para maiores informações ou sugestões, contacte a desenvolvedora da solução por meio do pamela.lunelli@gmail.com
            </StyledHelpContainer.Paragraph>
        </div>
    </StyledHelpContainer>
)

export default HelpContainer