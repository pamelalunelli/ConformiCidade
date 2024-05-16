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
            Esta aplicação foi desenvolvida como parte de um Trabalho de Conclusão de Curso (TCC) para facilitar a validação de modelos de entrada em sistemas tributários. Além disso, a aplicação gera relatórios detalhados de conformidade entre esses modelos de entrada e um modelo de referência, que é uma parte fundamental de um modelo maior que descreve o cadastro urbano.
            </StyledHelpContainer.Paragraph>

            <StyledHelpContainer.IntermediateTitle>
            Como Funciona
            </StyledHelpContainer.IntermediateTitle>
            <StyledHelpContainer.Paragraph>
            Validação de Modelos de Entrada: A aplicação permite que você insira os modelos de entrada de sistemas tributários para análise. Ela verifica a integridade e a precisão desses modelos em relação aos requisitos estabelecidos.
            Geração de Relatórios de Conformidade: Após a validação, a aplicação compara os modelos de entrada com o modelo de referência, identificando discrepâncias e inconsistências. Ela gera relatórios detalhados, destacando áreas de conformidade e sugerindo melhorias.
            </StyledHelpContainer.Paragraph>
            <StyledHelpContainer.IntermediateTitle>
            Utilizando a Aplicação
            </StyledHelpContainer.IntermediateTitle>
            <StyledHelpContainer.Paragraph>
            Carregando os Modelos de Entrada: Você pode carregar os modelos de entrada diretamente na aplicação. Certifique-se de que os formatos de arquivo são compatíveis (por exemplo, CSV, JSON, XML).
            Iniciando a Validade: Após carregar os modelos de entrada, inicie o processo de validação. A aplicação analisará os dados e fornecerá feedback instantâneo sobre sua conformidade com os padrões estabelecidos.
            Revisão dos Relatórios: Após a validação, você pode revisar os relatórios gerados pela aplicação. Eles destacarão áreas de conformidade e sugerirão ações corretivas, se necessário.
            </StyledHelpContainer.Paragraph>

            <StyledHelpContainer.IntermediateTitle>
            Suporte
            </StyledHelpContainer.IntermediateTitle>
            <StyledHelpContainer.Paragraph>
            Se você encontrar dificuldades durante o uso da aplicação ou tiver dúvidas sobre os resultados da validação, não hesite em entrar em contato conosco. Estamos aqui para ajudar e garantir uma experiência tranquila e eficiente.
            Agradecemos por utilizar nossa aplicação e esperamos que ela contribua significativamente para seus projetos de modelagem tributária e urbana.
            </StyledHelpContainer.Paragraph>
        </div>
    </StyledHelpContainer>
)

export default HelpContainer