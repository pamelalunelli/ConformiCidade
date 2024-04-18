import React, { useEffect, useState } from 'react';
import { Formik, Form, Field } from 'formik';
import { toast } from 'react-toastify';
import Slider from '../../library/slider';
import Loader from '../../library/loader';
import { StyledValidationModal } from './styles';
import { InfoCircleOutlined } from '@ant-design/icons'; // Importe o ícone necessário

const ValidationModal = ({
    modalIsOpen,
    closeModal,
    userData,
    userDataId 
}) => {
    const [defaultList, setDefaultList] = useState([]);
    const [isFetching, setIsFetching] = useState(true);
    const [currentSlide, setCurrentSlide] = useState(0);
    const [selectedField, setSelectedField] = useState(null); // Campo de referência selecionado

    const fetchObjetos = async () => {
        try {
            setIsFetching(true);
            const response = await fetch('/api/get_reference_fields/');
            const data = await response.json();
            console.log('Data fetched:', data);
            setDefaultList(data);
        } catch (error) {
            console.error('Error fetching data:', error);
            toast.error('Erro ao buscar objetos');
        } finally {
            setIsFetching(false);
        }
    };

    useEffect(() => {
        fetchObjetos();
    }, []);

    const parseUserData = (fieldName) => {
        if (userData && userData.topReferencesJSON) {
            const parsedData = JSON.parse(userData.topReferencesJSON);
            const fieldValues = parsedData[fieldName];
            if (fieldValues) {
                return fieldValues;
            }
        }
        return [];
    };    

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
                body: JSON.stringify({ ...values, userDataId }),
            });
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                window.open(url, '_blank');
                toast.success('Dados enviados com sucesso!');
                closeModal();
            } else {
                toast.error('Erro ao enviar dados.');
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            toast.error('Erro ao enviar dados');
        }
    };

    // Função para exibir informações detalhadas do campo de referência selecionado
    const showFieldDetails = (field) => {
        setSelectedField(field);
    };

    // Função para fechar o painel de informações detalhadas
    const closeFieldDetails = () => {
        setSelectedField(null);
    };

    return (
        <StyledValidationModal isOpen={modalIsOpen} onClose={closeModal} title={'Valide seus dados'} subtitle={'Lorem ipsum dolor sit amet consectetur. Nisi nec quis sagittis placerat amet amet ridiculus lorem.'} primaryButtonLabel={'Enviar'} btnType={'submit'}>
            {isFetching ? <Loader /> : (
                <Formik initialValues={initialValues} onSubmit={handleSubmit}>
                    {({ setFieldValue }) => (
                        <Form id={'validation-form-id'}>
                            <Slider totalSlides={defaultList.length} currentSlide={currentSlide} setCurrentSlide={setCurrentSlide}>
                                {defaultList.map(dl => (
                                    <StyledValidationModal.Container key={dl.name}>
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
                                            <StyledValidationModal.List.Title>&nbsp;</StyledValidationModal.List.Title> {/* Adicione um espaço em branco para manter o alinhamento */}
                                            <StyledValidationModal.List.Subtitle>Seus campos</StyledValidationModal.List.Subtitle>
                                            <StyledValidationModal.List>
                                                {dl.fields.map((field, i) => (
                                                    <li key={`${dl.name}-${i}`}>
                                                        <Field
                                                            component={StyledValidationModal.Select}
                                                            name={`${dl.name}.${field}`}
                                                            options={parseUserData(field).map(data => ({ value: data, label: data }))}
                                                            placeholder='Selecione...'
                                                            onChange={(e) => setFieldValue(`${dl.name}.${field}`, e.value)}
                                                        />
                                                    </li>
                                                ))}
                                            </StyledValidationModal.List>
                                        </div>
                                    </StyledValidationModal.Container>
                                ))}
                            </Slider>
                            {/* Exibir o painel de informações detalhadas */}
                            {selectedField && (
                                <div className="field-details-panel">
                                    <h3>{selectedField}</h3>
                                    <p>Texto genérico com informações sobre o campo de referência selecionado.</p>
                                    <button onClick={closeFieldDetails}>Fechar</button>
                                </div>
                            )}
                        </Form>
                    )}
                </Formik>
            )}
        </StyledValidationModal>    
    );
};

export default ValidationModal;