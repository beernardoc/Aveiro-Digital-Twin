import './EndSimulation.css';
import axios from "axios";
import { useState } from 'react';

export default function EndSimulation() {
    const [showModal, setShowModal] = useState(false); // State to manage modal visibility
    const [simulationName, setSimulationName] = useState('');

    const endsimulation = () => {
        axios.post('http://localhost:5000/api/endSimulation')
            .then(response => {
                if (response.status === 200) {
                    console.log('Solicitação enviada com sucesso:', response.data);
                    // remove blockedRoundabouts from sessionStorage
                    sessionStorage.removeItem('blockedRoundabouts');
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Erro ao enviar a solicitação:', error);
            });
    }

    const saveAndEndSimulation = () => {
        axios.post('http://localhost:5000/api/endSimulationAndSave?name=' + simulationName)
            .then(response => {
                if (response.status === 200) {
                    console.log('Solicitação enviada com sucesso:', response.data);
                    // remove blockedRoundabouts from sessionStorage
                    sessionStorage.removeItem('blockedRoundabouts');
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Erro ao enviar a solicitação:', error);
            });
    }

    const handleShow = () => {
        setShowModal(true);
    };

    // Function to handle closing the modal
    const handleClose = () => {
        setShowModal(false);
    };

    return (
        <>
            <div className="end-page-container">
                <div className="end-page">
                    <h1 style={{color: "black", fontSize: "40px", paddingBottom: "30px"}}>End the Simulation?</h1>
                    <div className="end-page-buttons">
                        <button className="end-button" type='submit' style={{ marginRight: '10px' }} onClick={endsimulation}>End the Simulation</button>
                        <button className="end-button" type='submit' onClick={handleShow}>Save and End the Simulation</button>
                    </div>
                    <p style={{ color: 'black', marginTop: '10px' }}>
                        Here you can end the simulation or save the simulation to your account history and then end it.
                    </p>
                </div>
            </div>

            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={handleClose}>&times;</span>
                        <p> Choose a Name for the Simulation </p>
                        <input type="text" placeholder="Simulation Name" style={{ width: "100%", height: "30px", marginBottom: "20px" }} onChange={(e) => setSimulationName(e.target.value)} />
                        <div className="modal-buttons">
                            <button type='submit' style={{ marginRight: "20px" }} onClick={saveAndEndSimulation}>Save Simulation</button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}