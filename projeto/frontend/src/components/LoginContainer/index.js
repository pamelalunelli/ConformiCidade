import React, { useState, useRef, useEffect } from 'react';
import { toast } from 'react-toastify';
import { Formik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { Link, useHistory } from 'react-router-dom';

import { usePaths } from '../Utils/utils';
import { useUser } from '../Utils/user-utils';
import { Eye, EyeSlash } from '../library/icons';
import { Field } from '../library/inputs';
import { useToken } from '../../TokenContext'; 
import Logo from '../../../static/images/logoSemFundo.png';

const schema = Yup.object().shape({
    username: Yup.string().required('Campo obrigatório'),
    password: Yup.string().required('Campo obrigatório'),
});

import { StyledLoginContainer } from './styles';
import { NoBgButton } from '../library/buttons';

const LoginContainer = () => {
    const paths = usePaths();
    const history = useHistory();
    const { updateUser } = useUser();
    const { setToken } = useToken();

    const isMounted = useRef(true);
    const [showPassword, setShowPassword] = useState(false);
    const [csrfToken, setCsrfToken] = useState('');
    const [isValid, setIsValid] = useState(false);
    const [isDirty, setIsDirty] = useState(false);

    useEffect(() => {
        
        const csrfTokenFromCookie = getCookie('csrftoken');
        setCsrfToken(csrfTokenFromCookie);
        return () => (isMounted.current = false);
    }, []);

    const handleSubmit = async (values, { setSubmitting, setErrors }) => {
        try {
            
            const response = await axios.post('/api/login/', values, { headers: { 'X-CSRFToken': csrfToken } });
            if (isMounted.current) {
                localStorage.setItem('token', response.data.token);
                localStorage.setItem('userInfo', JSON.stringify(response.data.user_info));

                const { token, ...userDetails } = response.data;
                updateUser(userDetails);
                setToken(token);

                history.push(paths.home());
            }
        } catch (error) {
            if (isMounted.current) {
                toast.error('Falha no login. Confira suas credenciais');
                setErrors({ general: 'Falha no login. Confira suas credenciais' });
            }
        } finally {
            if (isMounted.current) {
                setSubmitting(false);
            }
        }
    };

 
    const getCookie = (name) => {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        console.log(cookieValue)
        return cookieValue ? cookieValue.pop() : '';
    };

    useEffect(() => {
        setIsValid(schema.isValidSync({ username: '', password: '' }));
        setIsDirty(false);
    }, []);

    return (
        <StyledLoginContainer>
            <StyledLoginContainer.Container>
            <div style={{ textAlign: 'center', marginTop: '20px', marginBottom: '20px' }}>
                <img src={Logo} alt="Logo" style={{ width: '300px', height: 'auto' }} />
                </div>
                <Formik
                    initialValues={{ username: '', password: '' }}
                    validationSchema={schema}
                    onSubmit={handleSubmit}>
                    {({ errors, isSubmitting, values, handleChange }) => {
                        useEffect(() => {
                            setIsValid(schema.isValidSync(values));
                            setIsDirty(Object.values(values).some(Boolean));
                        }, [values]);

                        return (
                            <StyledLoginContainer.Form>
                                <Field
                                    type='text'
                                    name='username'
                                    id='username-id'
                                    label='Usuário'
                                    error={errors.username}
                                    placeholder='Digite seu usuário...'
                                    autoComplete='on'
                                    onChange={handleChange}
                                />
                                <Field
                                    type={showPassword ? 'text' : 'password'}
                                    name='password'
                                    id='password-id'
                                    label='Senha'
                                    autoComplete='current-password'
                                    after={
                                        <NoBgButton size='SMALL' onClick={() => setShowPassword(!showPassword)}>
                                            {showPassword ? <EyeSlash /> : <Eye />}
                                        </NoBgButton>
                                    }
                                    placeholder='Digite sua senha...'
                                    error={errors.password}
                                    onChange={handleChange}
                                />
                                <StyledLoginContainer.Submit type='submit' disabled={!isValid || isSubmitting || !isDirty}>
                                    Entrar
                                </StyledLoginContainer.Submit>
                            </StyledLoginContainer.Form>
                        );
                    }}
                </Formik>
                <StyledLoginContainer.RegisterMessage>
                    Não tem conta? <Link to={paths.signup()}>Criar conta</Link>
                </StyledLoginContainer.RegisterMessage>
            </StyledLoginContainer.Container>
        </StyledLoginContainer>
    );
};

export default LoginContainer;