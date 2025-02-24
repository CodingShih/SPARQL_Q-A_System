// src/UI/Burger/Burger.js
import React from 'react';
import { StyledBurger } from './Burger.styled';

const Burger = ({ isOpen, setIsOpen }) => {
  return (
    <StyledBurger onClick={() => setIsOpen(!isOpen)}>
      <div />
      <div />
      <div />
    </StyledBurger>
  );
}

export default Burger;
