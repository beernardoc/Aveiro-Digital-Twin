import logo from './logo.svg';
import './App.css';
import React from 'react';

import axios from 'axios';

const api = "http://localhost:5000/api";

function App() {


  function runPythonScript() {
    axios.post(`${api}/run`)
      .then(response => {
        console.log('Comando executado com sucesso:', response.data);
        // Faça algo com os dados retornados, se necessário
      })
      .catch(error => {
        console.error('Erro ao executar o comando:', error);
      });
  }

  

  return (
    <div className="App">
      <button onClick={runPythonScript}>RUN</button>
    </div>
  );
}

export default App;
