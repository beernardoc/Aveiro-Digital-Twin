import './ClearSimulation.css';
import axios from "axios";

export default function ClearSimulation() {
    const clearSimulation = () => {
        axios.get('http://localhost:5000/api/clearSimulation')
            .then(response => {
                if (response.status === 200) {
                    console.log('Solicitação enviada com sucesso:', response.data);
                    window.location.href = '/simulation';
                }
            })
            .catch(error => {
                console.error('Erro ao enviar a solicitação:', error);
            });
    }

    return (
        <div className="clear-page-container">
            <div className="clear-page">
                <h1 style={{color: "black", fontSize: "40px", paddingBottom: "30px"}}>Clear All the Vehicles from the Simulation</h1>
                <button className="clear-button" type='submit' onClick={clearSimulation}>Clear Vehicles</button>
            </div>
        </div>
    );
}