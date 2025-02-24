// src/SPARQLQA.js
import React, { useState } from 'react';
import AtomicSpinner from 'atomic-spinner';

function SPARQLQA() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false); // New loading state


  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // start loading

    try {
        const response = await fetch('http://127.0.0.1:5000/api/question', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: question }),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setAnswer(data.answer || `Error: ${data.error}`);
      } catch (error) {
        setAnswer(`Request failed: ${error.message}`);
      } finally {
        setLoading(false); // Stop loading
      }
    };

    return (
        <div className="qa-container">
        <h1>歡迎來到 SPARQL Q&A 系統</h1>
        <form onSubmit={handleSubmit} className="qa-form">
            <label>
            請輸入您的問題：
            <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
            />
            </label>
            <div className="submit-container">
                <button type="submit">送出</button>
            </div>
        </form>

        {/*loading && <div className="loading-animation">加載中...</div>*/}
        {loading && (
            <div className="loading-animation">查詢中
                <AtomicSpinner
                
                atomSize={150}
                displayElectronPaths={true}
                electronColorPalette={['#0081C9', '#5BC0F8', '#86E5FF']}
                electronSpeed={1}

                />
            </div>
            )}
            {/*atomSize={100}
                electronColorPalette={['#0081C9', '#5BC0F8', '#86E5FF']}
                electronSpeed={0.5}*/}



        {answer && (
            <div className="answer-section">
            <h2>答案：</h2>
            <pre>{answer}</pre>
            </div>
        )}
        </div>
    );
}

export default SPARQLQA;
