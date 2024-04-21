import React from 'react';
import axios from "axios";
import './Run2D_3D_form.css';

const Run2D_form = () => {

    const API = "http://localhost:5000/api";

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post(`${API}/run2D`);
            if (response.status === 200) {
                console.log('Solicitação enviada com sucesso:', response.data);
                window.location.href = '/simulation';
            }
        } catch (error) {
            console.error('Erro ao enviar a solicitação:', error);
        }
    };

    return (
        
        <div className='run2d-background'>
            <div className="overlay-run"></div> 
            <div className="content-above-overlay py-8 flex justify-center">
                <div className="mt-9 max-w-lg bg-white bg-opacity-80 rounded-lg p-8">
                    <form onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <label htmlFor="configFile" className="mb-1">Would you like to add a default
                                configuration file (.xml)?
                            </label>
                            <input
                                type="file"
                                id="configFile"
                                name="configFile"
                                accept=".xml"
                                className="w-full px-4 py-2 border rounded-md"
                            />
                        </div>
                        <div
                            className="mb-4 flex"> {/* Adicionado flex e items-center para alinhar o checkbox à esquerda */}
                            <div
                                className="inline-flex items-center"> {/* Adicionado para envolver o checkbox e o texto */}
                                <input
                                    type="checkbox"
                                    id="addRealData"
                                    name="addRealData"
                                    className="form-checkbox text-blue-500 h-5 w-5"
                                />
                                <span className="ml-2 text-sm">Add real data?</span>
                            </div>
                        </div>
                        <div className="mb-4">
                            <p className="text-sm text-gray-500 text-run">Now you will start the 2D digital twin of Aveiro city.
                                For this, it's necessary that you have Sumo properly installed on your computer.
                                Don't worry if you haven't added any configuration files at this step; during execution, you'll be able to dynamically adjust the simulation.</p>

                        </div>
                        <button type="submit" className="btn-2d-3d">Start Simulation</button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Run2D_form;
