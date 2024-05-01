import React, { useState } from 'react';
import './BlockRoundabout.css';
import map from '../asset/map/roundabouts_map.png';
import axios from 'axios';

export default function BlockRoundabout() {
    const [showModal, setShowModal] = useState(false); // State to manage modal visibility
    const [roundabout, setRoundabout] = useState(""); // State to manage selected roundabout [1, 2, 3, 4]
    const [blockedRoundabouts, setBlockedRoundabouts] = useState([]); // State to manage blocked roundabouts

    // Function to handle opening the modal
    const handleShow = (id) => {
        setRoundabout(id);
        setShowModal(true);
    };

    // Function to handle closing the modal
    const handleClose = (id) => {
        setShowModal(false);
    };

    // Function to block a roundabout
    const block_roundabout = () => {
        // Send a POST request to the server to block the selected roundabout
        // example: curl -X POST -d "" "http://localhost:5000/api/blockRoundabout?id=4"
        axios.post(`http://localhost:5000/api/blockRoundabout?id=${roundabout}`)
        .then(res => {
            console.log(res.data);
        });


        setBlockedRoundabouts([...blockedRoundabouts, roundabout]);
        handleClose();
    }

    return (
        <>
            <div className="roundabout-page-container">
                <div className="roundabout-page">
                    <h1 style={{ color: "black", fontSize: "40px" }}>Block a Roundabout</h1>
                    <h3 style={{ color: "black", fontSize: "20px", paddingBottom: "30px" }}>Select the roundabout you want to block</h3>
                    <div className="roundabout-page-map">
                        {/* Render the map image with clickable areas */}
                        <img src={map} alt="Roundabouts Map" useMap='#roundabout' />

                        {/* Define map areas with onClick events */}
                        <map name="roundabout">
                            <area shape="circle" coords="393,105,10" alt="Roundabout 1" style={{ cursor: "pointer" }} onClick={() => handleShow('1')} />
                            <area shape="circle" coords="551,275,10" alt="Roundabout 2" style={{ cursor: "pointer" }} onClick={() => handleShow('2')} />
                            <area shape="circle" coords="627,611,10" alt="Roundabout 3" style={{ cursor: "pointer" }} onClick={() => handleShow('3')} />
                            <area shape="circle" coords="915,415,10" alt="Roundabout 4" style={{ cursor: "pointer" }} onClick={() => handleShow('4')} />
                        </map>
                    </div>
                </div>
            </div>

            {/* Modal component */}
            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={handleClose}>&times;</span>
                        <p> Block Roundabout {roundabout}?</p>
                        <div className="modal-buttons">
                            <button className="modal-button-block" style={{ marginRight: "20px" }} onClick={block_roundabout}>Yes</button>
                            <button className="modal-button-unblock" onClick={handleClose}>No</button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}