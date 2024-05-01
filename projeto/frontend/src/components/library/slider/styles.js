import styled from 'styled-components';

export const StyledSlider = styled.div`
  position: relative;
`;

StyledSlider.Slide = styled.div(({ showSlide }) => `
  display: ${showSlide ? 'block' : 'none'};
`);

StyledSlider.Actions = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: 8px;
`;

StyledSlider.Dots = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin-bottom: ${({ theme }) => theme.spacing.xl}; /* Adjust margin-bottom as needed */
  overflow: hidden;
  position: relative;
`;

StyledSlider.Dot = styled.div(({ isSelected }) => `
  width: 20px;
  height: 20px;
  background: ${isSelected ? '#0049DD' : '#95B5F5'};
  border-radius: 100%;
  position: relative; /* Maintain relative positioning */
  cursor: pointer;
  font-size: 12px;
  color: ${isSelected ? '#FFFFFF' : '#000000'};
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1; /* Move dots to a higher z-index */
`);

StyledSlider.Line = styled.div`
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #95B5F5; /* Light blue color */
  /* Progress bar styling (remains unchanged) */
  &::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    width: ${({ progress }) => `${progress * 100}%`};
    height: 100%;
    border-radius: 3px;
    background-color: #0049DD;
    transform: translateY(-50%);
    transition: width 0.3s ease-in-out;
    z-index: 0; /* Move progress bar to a lower z-index */
  }
`;

export default StyledSlider;