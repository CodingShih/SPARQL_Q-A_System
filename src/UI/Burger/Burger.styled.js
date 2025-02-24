// src/UI/Burger/Burger.styled.js
import styled from 'styled-components';

export const StyledBurger = styled.button`
  position: absolute;
  top: 1rem;
  right: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 1.5rem;
  height: 2rem;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  
  div {
    width: 2rem;
    height: 0.25rem;
    background: #787676;
    border-radius: 10px;
    position: relative;
    transform-origin: 1px;
  }

  @media screen and (min-width: 576px) {
    div {
      visibility: hidden;
    }
  }

`;