import './ClearSimulation.css';

export default function ClearSimulation() {
    return (
        <div className="clear-page-container">
            <div className="clear-page">
                <h1 style={{color: "black", fontSize: "40px", paddingBottom: "30px"}}>Clear All the Vehicles from the Simulation</h1>
                <button className="clear-button" type='submit'>Clear Vehicles</button>
            </div>
        </div>
    );
}