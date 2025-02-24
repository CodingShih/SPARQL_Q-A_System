// CodeDisplay.js
import React from 'react';
import Prism from 'prismjs';
import 'prismjs/themes/prism.css';

function CodeDisplay({ code }) {
  const html = Prism.highlight(code, Prism.languages.python, 'python');
  return <pre dangerouslySetInnerHTML={{ __html: html }} />;
}

export default CodeDisplay;
