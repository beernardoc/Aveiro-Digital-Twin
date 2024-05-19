import './History.css';
import Card from '../components/HistoryCard';
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

export default function History() {
    const [history, setHistory] = useState([]);
    const navigate = useNavigate();
    const [showModal, setShowModal] = useState(false);
    const [showResimulateModal, setShowResimulateModal] = useState(false);
    const [currentId, setCurrentId] = useState('');
 
    useEffect(() => {
        axios.get(`http://localhost:5000/api/history`)
            .then((response) => {
                const result = response.data;
                // flip the array to show the most recent simulations first
                result.reverse();
                setHistory(result);
            })
            .catch((error) => {
                console.error('Erro ao executar o comando:', error);
            });
    }, []);

    const handleDelete = (_id) => {
        axios.delete(`http://localhost:5000/api/history?id=${_id}`)
            .then((response) => {
                console.log('Comando executado com sucesso:', response.data);
                setHistory(history.filter((history) => history._id.$oid !== _id));
            })
            .catch((error) => {
                console.error('Erro ao executar o comando:', error);
            });
    }

    const handleClick = (_id) => {
        // Redirect to the simulation page with the simulation id
        axios.get(`http://localhost:5000/api/sim_running`)
            .then((response) => {
                if (response.data.sim_running === false) {
                    axios.post(`http://localhost:5000/api/resimulation?id=${_id}`)
                        .then((response) => {
                            console.log('Comando executado com sucesso:', response.data);
                            navigate('/simulation');
                        })
                        .catch((error) => {
                            console.error('Erro ao executar o comando:', error);
                        });
                } else {
                    handleShow();
                }
            })
            .catch((error) => {
                console.error('Erro ao executar o comando:', error);
            });
    };

    const handleShow = () => {
        setShowModal(true);
    };

    // Function to handle closing the modal
    const handleClose = () => {
        setShowModal(false);
    };

    const handleResimulateShow = (_id) => {
        setCurrentId(_id);
        setShowResimulateModal(true);
    }

    const handleResimulateClose = () => {
        setShowResimulateModal(false);
    }


    
    return (
        <>
            <div className="history-page-container">
                <div className="history-page">
                    <h1 style={{color: "black", fontSize: "40px", paddingBottom: "30px", paddingTop: "50px"}}>Your Simulation History</h1>
                
                    <div className="history-page-historys" style={{ marginTop: "30px" }}>
                        <div className="history-page-history">
                            <div className="history">
                                {history.map((history) => (
                                    <Card key={history._id.$oid} id={history._id.$oid} date={history.date.$date} simulation_name={history.simulation_name} _id={history._id.$oid}
                                        handleClick={() => handleResimulateShow(history._id.$oid)} handleDelete={() => handleDelete(history._id.$oid)} />
                                ))}
                                {history.length === 0 && 
                                    <>
                                        <h2 style={{color: "black", fontSize: "20px", paddingBottom: "20px"}}>Your history is empty, make some simulations!</h2>
                                        <button type='submit' onClick={() => navigate('/')}>Make Simulations</button>
                                    </>
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={handleClose}>&times;</span>
                        <p> There is a simulation running. Please wait until it finishes, or close the running simulation. </p>
                        <div className="modal-buttons" style={{ marginTop: "20px" }}>
                            <button type='submit' style={{ marginRight: "20px" }} onClick={() => navigate("/endSimulation")}>End Simulation</button>
                        </div>
                    </div>
                </div>
            )}

            {showResimulateModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={handleResimulateClose}>&times;</span>
                        <p> What type of simulation do you want to do?</p>
                        <div className="modal-buttons" style={{ marginTop: "20px" }}>
                            <button type='submit' style={{ marginRight: "20px" }} onClick={() => handleClick(currentId)}>Run Simulation in <b>2D</b></button>
                            <button type='submit' style={{ marginRight: "20px" }} onClick={() => handleClick(currentId)}>Run Simulation in <b>3D</b></button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}