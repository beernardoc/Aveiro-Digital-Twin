import './EndSimulation.css';
import axios from "axios";

export default function EndSimulation() {
    const endsimulation = () => {
        axios.post('http://localhost:5000/api/endSimulation')
            .then(response => {
                if (response.status === 200) {
                    console.log('Solicitação enviada com sucesso:', response.data);
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Erro ao enviar a solicitação:', error);
            });
    }

    return (
        <div className="end-page-container">
            <div className="end-page">
                <h1 style={{color: "black", fontSize: "40px", paddingBottom: "30px"}}>End the Simulation?</h1>
                <div className="end-page-buttons">
                    <button className="end-button" type='submit' style={{ marginRight: '10px' }} onClick={endsimulation}>End the Simulation</button>
                    <button className="end-button" type='submit' onClick={endsimulation}>Save and End the Simulation</button>
                </div>
                <p style={{ color: 'black', marginTop: '10px' }}>
                    Here you can end the simulation or save the simulation to your account history and then end it.
                </p>
            </div>
        </div>
    );
}