import React from 'react';
import axios from 'axios';
import teste from '../asset/carla.jpg';
import './Run2D_3D_form.css';

const Run3D_form = () => {

    const API = "http://localhost:5000/api";

    const handleSubmit = async (event) => {

        event.preventDefault();  

        try {
            const response = await axios.post(`${API}/run3D`);
            if (response.status === 200) {
                console.log('Simulação 3D iniciada com sucesso:', response.data);
                window.location.href = '/simulation';
            }
        } catch (error) {
            console.error('Erro ao iniciar a simulação 3D:', error);
        }
    };

    return (

        <div className='run3d-background'>
            <div className="overlay-run"></div> 
            <div className="content-above-overlay py-8 flex justify-center">
                <div className="mt-9 max-w-lg bg-white bg-opacity-80 rounded-lg p-8">
                    <form onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <label htmlFor="configFile" className="mb-1">
                                Configuration File (.xml)
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
                            <p className="text-sm text-gray-600 text-run">
                                The 3D simulation will be performed using CARLA. Make sure your system meets the
                                following minimum requirements: Quad-core CPU, 8 GB RAM, NVIDIA GTX 1060. For best
                                performance, an NVIDIA RTX 2070 or higher GPU and 16 GB RAM are recommended.
                            </p>
                        </div>
                        <div className="text-center">
                            <button type="submit" className="btn-2d-3d"> Start Simulation </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Run3D_form;