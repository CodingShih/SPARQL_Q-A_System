// Navbar.js
import React, { useState } from 'react';

//import ReactDOM from 'react-dom/client'
import { Link } from 'react-router-dom';
import './Navbar.css';

//import Navbar from 'react-bootstrap/Navbar';
//import svgIcon from './navbaricon.svg';
//import Nav from 'react-bootstrap/Nav';
// 引入 Burger 和 Menu 组件
//import Burger from '../UI/Burger/Burger';
//import Menu from '../UI/Menu/Menu';

function NavbarComponent() {

  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    
  <div >
    {/*style={{width: '100%', height: '10vh'}}*/}
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-logo">
            JasonITxFianance
          </Link>
          {/*<Burger isOpen={isOpen} toggleMenu={toggleMenu} />

          <Burger isOpen={isOpen} setIsOpen={setIsOpen} />
          <Menu isOpen={isOpen} />


        <div className="burger-menu" onClick={toggleMenu}>
            <div className={isMenuOpen ? 'burger-bar clicked' : 'burger-bar unclicked'}></div>
            <div className={isMenuOpen ? 'burger-bar clicked' : 'burger-bar unclicked'}></div>
            <div className={isMenuOpen ? 'burger-bar clicked' : 'burger-bar unclicked'}></div>
          </div>*/}

          <div className="burger-menu" onClick={toggleMenu}>
            <div className={`burger-bar ${isMenuOpen ? 'clicked' : 'unclicked'}`}></div>
            <div className={`burger-bar ${isMenuOpen ? 'clicked' : 'unclicked'}`}></div>
            <div className={`burger-bar ${isMenuOpen ? 'clicked' : 'unclicked'}`}></div>
          </div>


          <div className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
            <ul>
              <li className="nav-item">
                <Link to="/" className="nav-links" onClick={toggleMenu}>
                  主頁
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/posts" className="nav-links" onClick={toggleMenu}>
                  我的Blog's
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/about" className="nav-links" onClick={toggleMenu}>
                  關於我
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/qa-system" className="nav-links" onClick={toggleMenu}>
                  SPARQL Q&A System
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}


export default NavbarComponent;
