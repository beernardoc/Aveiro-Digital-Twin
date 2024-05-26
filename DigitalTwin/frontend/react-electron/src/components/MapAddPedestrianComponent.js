import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapComponent.css';
import L from 'leaflet';
import {Tooltip} from "react-tooltip";
import axios from 'axios';

const initialMarkerIcon = new L.icon({
    iconUrl: 'https://cdn4.iconfinder.com/data/icons/location-45/68/pin_map_start_route-256.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const finalMarkerIcon = new L.icon({
    iconUrl: 'https://cdn1.iconfinder.com/data/icons/location-outline/91/Location_05-512.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
});

const MapAddCarComponent = () => {
    const [clickCount, setClickCount] = useState(0);
    const [initialPosition, setInitialPosition] = useState(null);
    const [finalPosition, setFinalPosition] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false); // Estado para controlar se o modal está aberto
    const [markerStart, setMarkerStart] = useState(null);

    const handleAddStart = () => {
        setClickCount(0);
        setMarkerStart(true);
    }

    const handleAddFinish = () => {
        setClickCount(1);
        setMarkerStart(false);
    }

    const handleMapClick = (e) => {
        const { lat, lng } = e.latlng;
        console.log(`Latitude: ${lat}, Longitude: ${lng}`);

        if (clickCount === 0) {
            setInitialPosition({ lat, lng });
        } else {
            setFinalPosition({ lat, lng });
        }
    };

    const handleRemoveMarkers = () => {
        setInitialPosition(null);
        setFinalPosition(null);
    };

    const handleSubmit = () => {
        setIsModalOpen(true); // Abrir o modal ao clicar em "Submit"
        console.log('Initial position:', initialPosition);
        console.log('Final position:', finalPosition);
    }

    const closeModal = () => {
        setIsModalOpen(false); // Fechar o modal
    }

    const insertCar = () => {
        var pedestrian = {};
        if (initialPosition && finalPosition) {
            pedestrian = {
                "start": {
                    "lng": initialPosition.lng,
                    "lat": initialPosition.lat
                },
                "end": {
                    "lng": finalPosition.lng,
                    "lat": finalPosition.lat
                }
            };


            }

         else if (initialPosition) {
            pedestrian = {
                "start": {
                    "lng": initialPosition.lng,
                    "lat": initialPosition.lat
                }
            };


        }
         else {
            pedestrian = {
                "end": {
                    "lng": finalPosition.lng,
                    "lat": finalPosition.lat
                }
            };
        }

        console.log('Car:', pedestrian);
        axios.post('http://localhost:5000/api/addSimulatedPedestrian', pedestrian)
                    .then(response => {
                        // Lida com a resposta da solicitação
                        console.log(response.data);
                    })
                    .catch(error => {
                        // Lida com erros na solicitação
                        console.error('Erro ao enviar objeto para a rota:', error);
                    });
    }

    return (
        <div>
            <MapContainer
                center={[40.63319824906938, -8.657974862473974]}
                zoom={16}
                className="map"
            >
                <TileLayer url="https://api.maptiler.com/maps/basic-v2/256/{z}/{x}/{y}.png?key=eKqBPyYHk8odwD7GfHAf" />
                {initialPosition && (
                    <Marker position={[initialPosition.lat, initialPosition.lng]} icon={initialMarkerIcon}>
                        <Popup>
                            Posição Inicial
                        </Popup>
                    </Marker>
                )}
                {finalPosition && (
                    <Marker position={[finalPosition.lat, finalPosition.lng]} icon={finalMarkerIcon}>
                        <Popup>
                            Posição Final
                        </Popup>
                    </Marker>
                )}

                <MapEventsHandler handleMapClick={handleMapClick} />
            </MapContainer>
            <div className="mt-5">
                <button className="btn-clear rounded" 
                        style={{width: '150px', backgroundColor: markerStart ? 'green' : '#F47065'}} 
                        onClick={handleAddStart}>Start Position
                </button>
                <button className="btn-clear rounded"
                        style={{width: '150px', backgroundColor: markerStart ?  '#F47065' : 'green' }} 
                        onClick={handleAddFinish}>Finish Position
                </button>
                <button className="btn-clear rounded"
                        style={{marginLeft: '200px'}} 
                        onClick={handleRemoveMarkers}>Clear markers
                </button>
                <button
                    className="btn-add-car rounded"
                    data-tooltip-id="Firsttooltip"
                    data-tooltip-content="You need to select at least one initial position"
                    data-tooltip-place="bottom"
                    onClick={handleSubmit}
                    disabled={!initialPosition} // Desativa o botão se initialPosition for null
                >
                    Add pedestrian
                </button>
            </div>
            <Tooltip id="Firsttooltip"/>


            {isModalOpen && (
                <div className="modal">
                    <div className="modal-content text-gray-500">
                        <span className="close" onClick={closeModal}>&times;</span>
                        <h2 className="mb-5 ">You are adding a pedestrian with the following parameters:</h2>

                        <form className="mt-3">
                            <label htmlFor="Quantity">Quantity:</label>
                            <input type="number" id="Quantity" name="speed" min="1" max="100" required
                                   defaultValue={1}/>
                            <br/>
                            <label htmlFor="Departure">Departure (s):</label>
                            <input type="number" id="Departure" name="orientationAngle" min="0" max="3600" required
                                   defaultValue={0}/>
                            <br/>

                            <p>From: {JSON.stringify(initialPosition)}</p>

                            {finalPosition ? (
                                <p>To: {JSON.stringify(finalPosition)}</p>
                            ) : (
                                <p>To: Random position</p>

                            )}


                        </form>
                        <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                                onClick={insertCar}>Submit
                        </button>


                    </div>
                </div>
            )}
        </div>
    );
};

const MapEventsHandler = ({handleMapClick}) => {
    useMapEvents({
        click: (e) => handleMapClick(e),
    });
    return null;
};

export default MapAddCarComponent;
