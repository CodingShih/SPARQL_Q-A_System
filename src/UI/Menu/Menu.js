// src/UI/Menu/Menu.js

import React from 'react';
import { StyledMenu } from './Menu.styled';

const Menu = ({ isOpen }) => {
  return (
    <StyledMenu isOpen={isOpen}>
      <a href="/">首頁</a>
      <a href="/macroeconomics">總體經濟</a>
    </StyledMenu>
  );
}

export default Menu;
