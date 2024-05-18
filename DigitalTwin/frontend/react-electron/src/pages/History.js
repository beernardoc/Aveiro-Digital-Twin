import './History.css';
import Card from '../components/HistoryCard';
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

export default function History() {
    const [history, setHistory] = useState([]);
    const navigate = useNavigate();

    const get_history = (id) => {

    }

    useEffect(() => {
        axios.get(`http://localhost:5000/api/history`)
            .then((response) => {
                console.log(response.data[0].date.$date);
                setHistory(response.data);
            })
            .catch((error) => {
                console.error('Erro ao executar o comando:', error);
            });
    }, []);
    
    return (
        <div className="history-page-container">
            <div className="history-page">
                <h1 style={{color: "black", fontSize: "40px", paddingBottom: "30px", paddingTop: "50px"}}>Your Simulation History</h1>
            
                <div className="history-page-historys" style={{ marginTop: "30px" }}>
                    <div className="history-page-history">
                        <div className="history">
                            {history.map((history) => (
                                <Card key={history._id.$oid} id={history._id.$oid} date={history.date.$date} simulation_name={history.simulation_name} handleClick={() => get_history(history.id)} />
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
    );
}