import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar'; 
import Sidebar from './components/Sidebar';
import SimulationPage from './pages/SimulationPage'; 
import CarPage from './pages/CarPage'; 
import './App.css';
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
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<><Sidebar /> <SimulationPage /></>} />
          <Route path="/car" element={<><Sidebar /> <CarPage /></>} />
          <Route path="/button" element={<><Sidebar /> <button onClick={runPythonScript}>RUN</button></>} />
        </Routes>
      </div>
    </Router>
 );
}

export default App;
