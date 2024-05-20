import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar'; 
import Sidebar from './components/Sidebar';
import SimulationPage from './pages/SimulationPage'; 
import CarPage from './pages/CarPage'; 
import './App.css';
import axios from 'axios';
import HomePage from "./pages/HomePage";
import Run2D from "./pages/Run2DPage";
import AddRandom from "./pages/AddRandom";
import Run3DPage from './pages/Run3DPage';
import ClearSimulation from './pages/ClearSimulation';
import Block from './pages/Block';
import BlockRoundabout from './pages/BlockRoundabout';
import BlockRoad from './pages/BlockRoad';
import Login from './pages/Login';
import Register from './pages/Register';
import Settings from './pages/Settings';
import EndSimulation from './pages/EndSimulation';
import History from './pages/History';
import { useState } from 'react';
import { useEffect } from 'react';

const api = "http://localhost:5000/api";

function App() {

  const [showSidebar, setShowSidebar] = useState(false);

  useEffect(() => {
    axios.get(`http://localhost:5000/api/sim_running`)
      .then((response) => {
          if (response.data.sim_running === false) {
              setShowSidebar(false);
          } else {
              setShowSidebar(true);
          }
      })
      .catch((error) => {
          console.error('Erro ao executar o comando:', error);
      });
  }, []);

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
          <Route path="/" element={<HomePage /> } />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/run2D" element={ <Run2D />} />
          <Route path="/run3D" element={<Run3DPage />} />
          <Route path="/car" element={<><Sidebar /> <CarPage /></>} />
          <Route path="/button" element={<><Sidebar /> <button onClick={runPythonScript}>RUN</button></>} />
          <Route path="/simulation" element={<><Sidebar /> <SimulationPage /></>} />
          <Route path="/addRandom" element={<><Sidebar /> <AddRandom /></>} />
          <Route path="/clear" element={ <><Sidebar /> <ClearSimulation /></> }></Route>
          <Route path="/block" element={<><Sidebar /> <Block /> </>} />
          <Route path="/block-roundabout" element={<><Sidebar /> <BlockRoundabout /> </>} />
          <Route path="/block-road" element={<><Sidebar /> <BlockRoad /> </>} />
          <Route path='/endSimulation' element={<><Sidebar /> <EndSimulation /></>} />
          <Route path="/history" element={
            <>
              {showSidebar && <Sidebar />}
              <History />
            </>
          } />
        </Routes>
      </div>
    </Router>
 );
}

export default App;
