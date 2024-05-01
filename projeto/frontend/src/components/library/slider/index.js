import React, { useState } from 'react';
import { PrimaryButton, SecondaryButton } from '../buttons';
import { StyledSlider } from './styles';

const Slider = ({
  children,
  currentSlide,
  setCurrentSlide,
  totalSlides,
}) => {
  const [selectedList, setSelectedList] = useState([currentSlide]);

  const nextSlide = () => {
    const nextIndex = currentSlide + 1;
    setSelectedList([...selectedList, nextIndex]);
    setCurrentSlide(nextIndex);
  };

  const previousSlide = () => {
    const previousIndex = currentSlide - 1;
    setSelectedList(selectedList.filter(index => index !== currentSlide));
    setCurrentSlide(previousIndex);
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