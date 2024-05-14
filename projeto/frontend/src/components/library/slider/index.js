import React, { useState, useEffect } from 'react';
import { PrimaryButton, SecondaryButton } from '../buttons';
import { StyledSlider } from './styles';
import { useToken } from '../../../TokenContext.js';

const Slider = ({
  children,
  currentSlide,
  setCurrentSlide,
  totalSlides,
  values,
  userDataId
}) => {
  const [selectedList, setSelectedList] = useState([currentSlide]);
  const { token } = useToken();

  useEffect(() => {
    handleAutosave(values);
    settingAutosavedFields(); // Chamada para a função de configuração de campos salvos automaticamente
  }, [currentSlide, values]);

  const handleAutosave = async (values) => {
    try {
      const response = await fetch('/api/autosave/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
      },
        body: JSON.stringify({ ...values, userDataId }),
      });
      if (!response.ok) {
        throw new Error('Erro ao salvar dados.');
      }
    } catch (error) {
      console.error('Erro ao salvar dados:', error);
    }
  };

  const settingAutosavedFields = async () => {
    try {
      const response = await fetch('/api/identifying_autosaved_fields/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify({ userDataId }),
      });
  
      if (!response.ok) {
        throw new Error('Erro ao salvar dados.');
      }
    } catch (error) {
      // Lidar com erros, se necessário
      console.error('Erro ao executar a chamada à API:', error);
    }
  };

  const nextSlide = async () => {
    const nextIndex = currentSlide + 1;
    setSelectedList([...selectedList, nextIndex]);
    setCurrentSlide(nextIndex);
    await handleAutosave(values);
  };

  const previousSlide = async () => {
    const previousIndex = currentSlide - 1;
    setSelectedList(selectedList.filter(index => index !== currentSlide));
    setCurrentSlide(previousIndex);
    await handleAutosave(values);
  };

  return (
    <StyledSlider>
      <StyledSlider.Dots>
        {[...Array(totalSlides).keys()].map(index => (
          <StyledSlider.Dot
            key={index}
            isSelected={selectedList.includes(index)}
            onClick={() => setCurrentSlide(index)}
          >
            {index + 1}
          </StyledSlider.Dot>
        ))}
        <StyledSlider.Line progress={currentSlide / (totalSlides - 1)} />
      </StyledSlider.Dots>
      {React.Children.toArray(children).map((child, i) => (
        <StyledSlider.Slide key={i} showSlide={i === currentSlide}>
          {child}
        </StyledSlider.Slide>
      ))}
      <StyledSlider.Actions>
        <SecondaryButton disabled={currentSlide === 0} size="SMALL" onClick={previousSlide}>
          Anterior
        </SecondaryButton>
        <PrimaryButton disabled={(currentSlide + 1) >= totalSlides} size="SMALL" onClick={nextSlide}>
          Próximo
        </PrimaryButton>
      </StyledSlider.Actions>
    </StyledSlider>
  );
};

export default Slider;