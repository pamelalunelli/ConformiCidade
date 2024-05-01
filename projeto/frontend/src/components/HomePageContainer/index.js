import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { Formik } from 'formik';
import * as Yup from 'yup';
import { getCookie } from '../Utils/cookieUtils';
import MatchingsNotConcluded from './MatchingsNotConcluded';
import { InputFile, Field } from '../library/inputs';
import ValidationModal from './ValidationModal';
import ClipLoader from "react-spinners/ClipLoader";
import { StyledHomePageContainer } from './styles';
import ERDiagram from '../../../static/images/ERDiagram.jpg'


const fileSchema = (required) => {
  return Yup.mixed().test('csv_arq', 'É necessário fornecer um arquivo', (value) => {
    if (!required) {
      return true;
    }
    return !!value;
  });
};

const schema = Yup.object().shape({
  fileName: Yup.string(),
  csv_arq: fileSchema(true),
});

const HomePageContainer = () => {
  const [modalIsOpen, setIsOpen] = useState(false);
  const [userData, setUserData] = useState(null);
  const [csrfToken, setCsrfToken] = useState('');
  const [userDataId, setUserDataId] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false); // State for spinner visibility

  useEffect(() => {
    const csrftoken = getCookie('csrftoken');
    setCsrfToken(csrftoken);
  }, []);

  const openModal = () => setIsOpen(true);

  const closeModal = () => setIsOpen(false);

  const handleSubmit = async (values, { resetForm }) => {
    setIsSubmitting(true);

    const formData = new FormData();
    formData.append('csv_arq', values.csv_arq);
    formData.append('csrfmiddlewaretoken', csrfToken);

    try {
      const response = await axios.post('/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': csrfToken,
        },
      });

      if (response.status === 200) {
        const userDataId = response.data.id;
        setUserDataId(userDataId);

        const fieldsCSV = response.data.fields;
        const tableNameCSV = response.data.tableName;

        try {
          const matchingTableName = await axios.post(
            `/api/create_matching_table/`,
            tableNameCSV,
            { headers: { 'Content-Type': 'application/json' } }
          );

          const userDataResponse = await axios.post(
            `/api/populate_matching_fields/`,
            { matchingTableName, fieldsCSV, userDataId },
            { headers: { 'Content-Type': 'application/json' } }
          );

          setUserData(userDataResponse.data);
          openModal();
          resetForm();
        } catch (userDataError) {
          toast.error('Erro ao obter dados do usuário');
        }
      } else {
        toast.error('Ocorreu um erro ao enviar seu arquivo');
      }
    } catch (error) {
      toast.error('Ocorreu um erro ao enviar seu arquivo');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <div>
        <StyledHomePageContainer.Title>Validador de Dados Cadastrais</StyledHomePageContainer.Title>
        <StyledHomePageContainer.Paragraph>
          Este validador tem como objetivo auxiliar o mapeamento das entidades presentes nos Cadastros Imobiliários Fiscais dos municípios tendo como base um modelo concebido a partir do segmento fiscal do modelo proposto por Santos (2022), tese de doutorado que teve como objeto de estudo os Direitos, Restrições e Responsabilidades (RRR) sob o aspecto técnico da ISO 19.152:2012 (Land Administration Domain Model).
        </StyledHomePageContainer.Paragraph>
      </div>
      <StyledHomePageContainer.Reference>
        <div>
          <StyledHomePageContainer.Reference.Title>
            Arquivo de Entrada
          </StyledHomePageContainer.Reference.Title>
          <StyledHomePageContainer.Paragraph>
            O arquivo a ser carregado deve ser um comma-separated value (*.csv) ou de texto (*.txt) e deve conter, obrigatoriamente, em sua primeira linha, os nomes dos campos a serem mapeados no processo. O arquivo pode ou não conter dados.
          </StyledHomePageContainer.Paragraph>
        </div>
        <StyledHomePageContainer>
          <div style={{ textAlign: 'center' }}>
            <a href={ERDiagram} target="_blank" rel="noopener noreferrer">
              <img src={ERDiagram} alt="Diagrama Entidade-Relacionamento" height="200" />
            </a>
            <StyledHomePageContainer.Paragraph>
              Clique na imagem para <br /> ampliar o diagrama
            </StyledHomePageContainer.Paragraph>
          </div>
        </StyledHomePageContainer>
      </StyledHomePageContainer.Reference>
      <Formik initialValues={{fileName: '', csv_arq: null}}
              validationSchema={schema}
              onSubmit={handleSubmit}>
        {({erros, isValid, dirty, setFieldValue}) => (
          <StyledHomePageContainer.Form>
            <Field label='Dê um nome para seu arquivo (opcional)'
                    id='file-name-id'
                    name='fileName'
                    placeholder='Digite um nome para seu arquivo...'/>
            <Field label='Selecione um arquivo'
                    id='file-id'
                    name='csv_arq'
                    placeholder='Selecionar arquivo...'
                    accept='.csv'
                    onChange={(e) => {
                      setFieldValue('csv_arq', e.currentTarget.files[0])
                    }}
                    as={InputFile}/>
            <StyledHomePageContainer.Form.Submit type='submit' disabled={!isValid || isSubmitting || !dirty}>
              {isSubmitting ? (
                <ClipLoader // Use the ClipLoader component
                  size={35} // Adjust size as needed
                  color={'#ffffff'} // Customize color
                />
              ) : (
                <span>Enviar</span>
              )}
            </StyledHomePageContainer.Form.Submit>
          </StyledHomePageContainer.Form>
        )}
      </Formik>
      <StyledHomePageContainer>
        <MatchingsNotConcluded />
      </StyledHomePageContainer>
      <ValidationModal modalIsOpen={modalIsOpen} closeModal={closeModal} userData={userData} userDataId={userDataId} /> {/* Pass userDataId to ValidationModal */}
    </>
  );
};

export default HomePageContainer;