import React, { useEffect, useState } from 'react';
import { Formik, Form, Field } from 'formik';
import { toast } from 'react-toastify';
import Slider from '../../library/slider';
import Loader from '../../library/loader';
import { StyledValidationModal, InfoIcon, CloseButton } from './styles';
import { SecondaryButton } from './styles';
import { InfoCircleOutlined } from '@ant-design/icons';
import { useToken } from '../../../TokenContext.js';

import axios from 'axios';

const ValidationModal = ({
    modalIsOpen,
    closeModal,
    userData,
    userDataId,
    matchingTableName,
    isOpenFromMatchings
}) => {
    const { token } = useToken();
    const [defaultList, setDefaultList] = useState([]);
    const [isFetching, setIsFetching] = useState(true);
    const [currentSlide, setCurrentSlide] = useState(0);
    const [selectedField, setSelectedField] = useState(null);
    const [userChoices, setUserChoices] = useState({});
    const [fieldDescription, setFieldDescription] = useState('');
    const [isLoadingUserChoices, setLoadingUserChoices] = useState(false);

    useEffect(() => {
        fetchObjetos();
        if (isOpenFromMatchings) {
            fetchUserChoices();
        }
    }, []);

    useEffect(() => {
        // Fecha a janela lateral quando o slide atual mudar
        setSelectedField(null);
    }, [currentSlide]);

    const fetchObjetos = async () => {
        try {
            setIsFetching(true);
            const response = await fetch('/api/get_reference_fields/', {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                }
            });
            if (!response.ok) {
                throw new Error('Erro ao buscar objetos');
            }
            const data = await response.json();
            //console.log('Data fetched:', data);
            setDefaultList(data);
        } catch (error) {
            console.error('Error fetching data:', error);
            toast.error('Erro ao buscar objetos');
        } finally {
            setIsFetching(false);
        }
    };

    const fetchUserChoices = async () => {
        try {
            setLoadingUserChoices(true)

            const response = await axios.post('/api/get_user_choices/', {
                matchingTableName
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                }
            });
            if (!response.status === 200) {
                throw new Error('Erro ao buscar seleções prévias do usuário');
            }
            const data = response.data;
            
            setUserChoices(data);
        } catch (error) {
            console.error('Error fetching user choices:', error);
        } finally {
            setLoadingUserChoices(false);
        }
    };

    const parseUserData = (fieldName) => {
        if (userData && userData.topReferencesJSON) {
            const parsedData = JSON.parse(userData.topReferencesJSON);
            const fieldValues = parsedData[fieldName];
            const decodedFieldName = fieldName.replace(/\\u([\d\w]{4})/gi, (match, grp) => String.fromCharCode(parseInt(grp, 16)));
            if (fieldValues && (decodedFieldName === 'SUGESTÃO' || decodedFieldName === 'ORDEM ALFABÉTICA')) {
                return null; 
            }
            if (fieldValues) {
                return fieldValues;
            }
        }
        return [];
    };
    //console.log('User choices:', userChoices);
    const initialValues = defaultList.reduce((acc, modelo) => {
        acc[modelo.name] = modelo.fields.reduce((fields, campo) => {
            fields[campo] = '';
            return fields;
        }, {});
        return acc;
    }, {});

    const handleSubmit = async (values) => {
        try {
            const response = await fetch('/api/process_form/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify({ ...values, userDataId })
            });
            if (!response.ok) {
                throw new Error('Erro ao enviar dados');
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            window.open(url, '_blank');
            toast.success('Dados enviados com sucesso!');
            closeModal();
            await fetch('/api/is_concluded/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify({ userDataId: userDataId, isConcluded: true })
            });            
        } catch (error) {
            console.error('Error submitting form:', error);
            toast.error('Erro ao enviar dados');
        }
    };

    const showFieldDetails = async (field) => {
        setSelectedField(field);
        try {
            // Envia o nome do campo clicado para o backend
            const response = await axios.post('/api/field_description/', {
                clickedField: field
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                }
            });
            if (!response.status === 200) {
                throw new Error('Erro ao buscar descrição do campo');
            }
            const data = response.data;
            console.log('Field description:', data);
            setFieldDescription(data.fieldDescription);
        } catch (error) {
            console.error('Error fetching field description:', error);
        }
    };

    const closeFieldDetails = () => {
        setSelectedField(null);
        setFieldDescription('');
    };
    //console.log(userChoices)
    return (
        <StyledValidationModal isOpen={modalIsOpen} onClose={closeModal} title={'Valide seus dados'} subtitle={'Para cada campo da esquerda (modelo de referência), encontre o correspondente no seu modelo de entrada. Caso não encontre correspondência, você pode deixar o campo vazio.'} primaryButtonLabel={'Enviar'} btnType={'submit'}>
            {(isFetching || isLoadingUserChoices) ? <Loader /> : (
                <div className="modal-content">
                    {selectedField && (
                        <div className="field-details-panel">
                            <h3>{selectedField}</h3>
                            <p>{fieldDescription}</p>
                            <CloseButton onClick={closeFieldDetails} size="SMALL">Fechar</CloseButton>
                        </div>
                    )}
                    <div className="form-content">
                        <Formik initialValues={{...initialValues, ...(!!userChoices && {...userChoices})}} onSubmit={handleSubmit}>
                            {({ setFieldValue, values }) => (  //console.log(values),
                                <Form id={'validation-form-id'}>
                                    <Slider
                                        totalSlides={defaultList.length}
                                        currentSlide={currentSlide}
                                        setCurrentSlide={(slide) => {
                                            setCurrentSlide(slide);
                                            setSelectedField(null); // Fecha a janela lateral ao trocar de slide
                                        }}
                                        values={values}
                                        userDataId={userDataId}
                                    >
                                        {defaultList.map((dl, index) => (
                                        <StyledValidationModal.Container key={index}>
                                        <div>
                                            <StyledValidationModal.List.Title>{dl.name}</StyledValidationModal.List.Title>
                                            <StyledValidationModal.List.Subtitle>Campos de Referência</StyledValidationModal.List.Subtitle>
                                            <StyledValidationModal.List>
                                                {dl.fields.map((field, i) => (
                                                    <li key={i} onClick={() => showFieldDetails(field)}>
                                                        <StyledValidationModal.List.FakeSelect>
                                                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                                                {field}
                                                                <InfoCircleOutlined style={{ marginLeft: '5px' }} />
                                                            </div>
                                                        </StyledValidationModal.List.FakeSelect>
                                                    </li>
                                                ))}
                                            </StyledValidationModal.List>
                                        </div>
                                        <div>
                                            <StyledValidationModal.List.Title>&nbsp;</StyledValidationModal.List.Title>
                                            <StyledValidationModal.List.Subtitle>Seus campos</StyledValidationModal.List.Subtitle>
                                            <StyledValidationModal.List>
                                                {dl.fields.map((field, i) => (
                                                    <li key={`${dl.name}-${i}`}>
                                                        {field === 'SUGESTÃO' || field === 'ORDEM ALFABÉTICA' ? (
                                                            <StyledValidationModal.DisabledField key={`${dl.name}-${i}`}>
                                                                {field}
                                                            </StyledValidationModal.DisabledField>
                                                        ) : ( console.log("values:", values[dl.name][field]),
                                                                //console.log("field:", field),
                                                                //console.log("dl:", dl),
                                                            <Field
                                                                component={StyledValidationModal.Select}
                                                                name={`${dl.name}.${field}`}
                                                                options={parseUserData(field).map(data => ({ value: data, label: data }))}
                                                                placeholder='Selecione...'
                                                                onChange={(e) => setFieldValue(`${dl.name}.${field}`, e.value)}
                                                                menuPlacement='auto'
                                                                menuPortalTarget={document.body}
                                                                {...(!!values[dl.name][field] && {defaultValue: {value: values[dl.name][field], label: values[dl.name][field]}})}
                                                                //defaultValue={{value: values[dl.name][field], label: values[dl.name][field]}}
                                                            />
                                                        )}
                                                    </li>
                                                ))}
                                            </StyledValidationModal.List>
                                        </div>
                                    </StyledValidationModal.Container>
                                ))}
                            </Slider>
                        </Form>
                    )}
                </Formik>
            </div>
        </div>
    )}
</StyledValidationModal>    
); 
};

export default ValidationModal;