import './Block.css';
import socketIOClient from 'socket.io-client';
import Card from '../components/BlockedCard';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Block() {

    const [message, setMessage] = useState('');
    const [blockedRoundabouts, setBlockedRoundabouts] = useState(null);

    const blockRoundabout = () => {
        window.location.href = '/block-roundabout';
    }

    useEffect(() => {
        const socket = socketIOClient('http://localhost:5000'); 

        socket.on('blocked_roundabouts', (data) => {
            // Convert the ArrayBuffer message to a string
            const decoder = new TextDecoder();
            const decodedMessage = decoder.decode(data);
            
            setMessage(decodedMessage);

            // Convert the JSON string to a JavaScript object
            const parsed = JSON.parse(decodedMessage);
            // it is a map, get the keys and convert to an array
            const blocked_roundabouts = Object.keys(parsed.blocked_roundabouts)
            setBlockedRoundabouts(blocked_roundabouts);
        });

        return () => socket.disconnect();
    }, []);

    const handle_unblock_roundabout = (id) => {
        axios.post(`http://localhost:5000/api/unblockRoundabout?id=${id}`)
        .then(res => {
            console.log(res.data);
        });
    }
  
    return (
        <div className="block-page-container">
            <div className="block-page">
                <h1 style={{color: "black", fontSize: "40px", paddingBottom: "30px"}}>Block a Road Segment</h1>
                
                <div className="block-page-buttons">
                    {/* 2 buttons, one to block roundabout and another to road */}
                    <button className="block-page-button" type='submit' onClick={blockRoundabout} style={{ marginRight: "30px" }}>Block Roundabout</button>
                    <button className="block-page-button" type='submit'>Block Road</button>
                </div>

                <div className="block-page-blocks" style={{ marginTop: "30px" }}>
                    <div className="block-page-block">
                        <h3 style={{color: "black", fontSize: "20px", paddingBottom: "10px"}}>Active Blocks</h3>
                        <div className="blocked-roundabouts">
                            <h2 style={{ color: "black", fontSize: "30px", marginTop: "20px" }}>Blocked Roundabouts</h2>
                            {blockedRoundabouts && blockedRoundabouts.map((roundabout, index) => (
                                <div key={index} className="blocked-roundabout">
                                    <Card id={roundabout} type="roundabout" handleClick={() => handle_unblock_roundabout(roundabout)} />
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}