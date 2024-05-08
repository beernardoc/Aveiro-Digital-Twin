import React, {useState} from 'react';
import teste from '../asset/teste.png';
import axios from "axios";
import {Tooltip} from "react-tooltip";
import {renderToString} from "react-dom/server"; // Importe a imagem de fundo




const AddRandomPedestrian_form = () => {

    const API = "http://localhost:5000/api";
    const [pedestrianQuantity, setPedestrianQuantity] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post(`${API}/addRandomPedestrian?qtd=${pedestrianQuantity}`);
            if (response.status === 200) {
                console.log('Solicitação enviada com sucesso:', response.data);
                window.location.href = '/simulation';
            }
        } catch (error) {
            console.error('Erro ao enviar a solicitação:', error);
        }
    };



    return (

        <div className="container mx-auto px-4 py-8 flex items-center justify-center">
            <div className="w-full max-w-lg bg-white bg-opacity-90 rounded-lg shadow-lg p-8">
                <form>
                    <div className="mb-4">
                        <label htmlFor="configFile" className="text-gray-500 block mb-1">How many pedestrians do you want to add?</label>
                        <input
                            type="number"
                            id="quantity"
                            className="w-full px-4 py-2 border rounded-md text-gray-700 focus:outline-none focus:border-green-500"
                            onChange={(e) => setPedestrianQuantity(e.target.value)}
                        />
                        <Tooltip id="Firsttooltip"/>
                    </div>

                    <div className="mb-4">
                        <p className="text-sm text-gray-500">You are adding pedestrians dynamically and randomly, meaning they will have random routes and behaviors.</p>
                        <p className="text-sm text-gray-500">You can see the pedestrians in the SUMO interface.</p>

                    </div>
                    <div className="text-center button-container">
                        <button onClick={handleSubmit}
                        >Add random pedestrians
                        </button>
                    </div>
                </form>
            </div>


        </div>
    );
};

export default AddRandomPedestrian_form;
