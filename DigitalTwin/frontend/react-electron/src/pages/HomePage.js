import React from 'react';
import { Tooltip } from 'react-tooltip';
import './Homepage.css';


const HomePage = () => {

    const handleClick = () => {
        if (sessionStorage.getItem('access_token') === null) {
            // Pass state variable indicating login is required
            window.location.href = '/login?required=true';
        } else {
            window.location.href = '/run2D';
        }
    }
    
    const handleClick3D = () => {
        if (sessionStorage.getItem('access_token') === null) {
            // Pass state variable indicating login is required
            window.location.href = '/login?required=true';
        } else {
            window.location.href = '/run3D';
        }
    }
    

    return (    

        <div className="homepage-background">

            <div className="overlay"></div> 
            <div className="container content-above-overlay mx-auto pt-20 mt-20">
                
                <div className="text-center mb-20">
                    <h1 className="text-h1-home">AVEIRO</h1>
                    <h1 className="text-h1-home">Digital Twin</h1>
                </div> 
                <div className="flex justify-center">
                    <button
                        data-tooltip-id="Firsttooltip"
                        data-tooltip-content="Make sure you have SUMO installed"
                        data-tooltip-place="bottom"
                        className="mr-5 btn-2d-3d py-6 px-12 mr-4"
                        onClick={handleClick}
                    >
                        Run simulation in <b>2D</b>
                    </button>
                    <button
                        data-tooltip-id="Secondtooltip"
                        data-tooltip-content="Make sure you have SUMO and CARLA installed"
                        data-tooltip-place="bottom"
                        className="ml-5 btn-2d-3d py-6 px-12"
                        data-tip="Outro texto do Tooltip para 3D"
                        data-for="botao3DTooltip"
                        onClick={handleClick3D}
                    >
                        Run simulation in <b>3D</b>
                    </button>
                </div>
            <Tooltip id="Firsttooltip"/>
            <Tooltip id="Secondtooltip"/>
            </div>
        </div>
    );
};

export default HomePage;