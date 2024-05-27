import React, { useState, useEffect } from 'react';
import axios from "axios";
import './Run2D_3D_form.css';

const Run2D_form = () => {

    const API = "http://localhost:5000/api";

    const handleSubmit = async (event) => {
        event.preventDefault();
        console.log(selectedOption, selectedEntities);

        try {
            let response = null;
            if (selectedOption === 'liveData')
                response = await axios.post(`${API}/run2D?live=True`, { entities: selectedEntities });

            else if (selectedOption === 'realData') {

                const startDateTimeString = `${selectedDay}T${startTime}:00.000Z`;
                const endDateTimeString = `${selectedDay}T${endTime}:00.000Z`;

                const startDateTime = new Date(startDateTimeString);
                const endDateTime = new Date(endDateTimeString);

                const formattedStartTime = startDateTime.toISOString();
                const formattedEndTime = endDateTime.toISOString();


                response = await axios.post(`${API}/run2D?realdata=True`, {
                    entities: selectedEntities,
                    startTime: formattedStartTime,
                    endTime: formattedEndTime
                });
            }

            else
                response = await axios.post(`${API}/run2D`, { entities: selectedEntities });

            if (response.status === 200) {
                console.log('Solicitação enviada com sucesso:', response.data);
                setShowError(false);  
                setErrorMessage('');  
                window.location.href = '/simulation';
            }
        } catch (error) {
            console.error('Erro ao enviar a solicitação:', error);
            if (error.response && error.response.status >= 500) {
                if (selectedOption === 'liveData')
                    setErrorMessage("Live Data not available at the moment. Please try again later. Error 500");
                if (selectedOption === 'realData')
                    setErrorMessage("Real Data not available at the moment. Please try again later. Error 500");
            } else {
                if (selectedOption === 'liveData')
                    setErrorMessage("Live Data not available at the moment. Please try again later.");
                if (selectedOption === 'realData')
                    setErrorMessage("Real Data not available at the moment. Please try again later.");
            }
            setShowError(true);  
        }
    };

    const [errorMessage, setErrorMessage] = useState('');
    const [showError, setShowError] = useState(false);
    const [selectedOption, setSelectedOption] = useState(null);
    const [selectedDay, setSelectedDay] = useState('');
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [maxDate, setmaxDate] = useState('');
    const [selectedEntities, setSelectedEntities] = useState([]);

    const entityTypes = ['Car', 'Bus', 'Bicycle', 'Motorcycle', 'Person'];

    useEffect(() => {
        const currentDate = new Date();
        const formattedDate = currentDate.toISOString().split('T')[0];
        setmaxDate(formattedDate);
      }, []);

    const handleOptionChange = (event) => {
        const value = event.target.value;
        if (selectedOption === value) {
            setSelectedOption(null);
        } else {
            setSelectedOption(value);
        }
    };

    const handleDayChange = (event) => {
        setSelectedDay(event.target.value);
    };

    const handleTimeChange = (event) => {
        if (event.target.name === 'startTime') {
            setStartTime(event.target.value);
        } else {
            setEndTime(event.target.value);
        }
    };

    const handleEntityChange = (event) => {
        const checked = event.target.checked;
        const value = event.target.value;
        setSelectedEntities(prev => {
            if (checked && !prev.includes(value)) {
                return [...prev, value];
            } else {
                return prev.filter(item => item !== value);
            }
        });
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
                        
                        <div className="mb-4 flex">
                            <div className="inline-flex items-center">
                                <input
                                    type="radio"
                                    id="liveData"
                                    name="dataOption"
                                    value="liveData"
                                    checked={selectedOption === 'liveData'}
                                    onClick={handleOptionChange}
                                    className="form-checkbox text-blue-500 h-5 w-5"
                                />
                                <label htmlFor="liveData" className="ml-2 text-sm">Live Data</label>
                            </div>
                            <div className="inline-flex items-center ml-4">
                                <input
                                    type="radio"
                                    id="realData"
                                    name="dataOption"
                                    value="realData"
                                    checked={selectedOption === 'realData'}
                                    onClick={handleOptionChange}
                                    className="form-checkbox text-blue-500 h-5 w-5"
                                />
                                <label htmlFor="realData" className="ml-2 text-sm">Real Data</label>
                            </div>
                        </div>

                        {selectedOption === 'realData' && (
                            <div>
                                <div className="mb-4">
                                    {entityTypes.map((type) => (
                                        <div key={type} className="flex items-center mb-2">
                                            <input
                                                type="checkbox"
                                                id={type}
                                                value={type}
                                                checked={selectedEntities.includes(type)}
                                                onChange={handleEntityChange}
                                                className="form-checkbox text-blue-500 h-5 w-5"
                                            />
                                            <label htmlFor={type} className="ml-2 text-sm">{type}</label>
                                        </div>
                                    ))}
                                </div>
                                <div className="mb-4">
                                    <label htmlFor="day" className="block text-sm font-medium text-gray-700">Day:</label>
                                    <input
                                        type="date"
                                        id="day"
                                        name="day"
                                        max={maxDate}
                                        value={selectedDay}
                                        onChange={handleDayChange}
                                        className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                    />
                                </div>
                                <div className="mb-4 flex">
                                    <div className="w-1/2">
                                        <label htmlFor="startTime" className="block text-sm font-medium text-gray-700">Start Time:</label>
                                        <input
                                            type="time"
                                            id="startTime"
                                            name="startTime"
                                            value={startTime}
                                            onChange={handleTimeChange}
                                            className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                        />
                                    </div>
                                    <div className="w-1/2 ml-4">
                                        <label htmlFor="endTime" className="block text-sm font-medium text-gray-700">End Time:</label>
                                        <input
                                            type="time"
                                            id="endTime"
                                            name="endTime"
                                            value={endTime}
                                            onChange={handleTimeChange}
                                            className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                        />
                                    </div>
                                </div>
                            </div>
                        )}

                        <div className="mb-4">
                            <p className="text-sm text-gray-500 text-run">Now you will start the 2D digital twin of Aveiro city.
                                For this, it's necessary that you have Sumo properly installed on your computer.
                                Don't worry if you haven't added any configuration files at this step; during execution, you'll be able to dynamically adjust the simulation.</p>

                        </div>

                        {showError && (
                            <div className="my-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4" role="alert">
                                <p className="font-bold">Atention!</p>
                                <p>{errorMessage}</p>
                            </div>
                        )}
                    
                        <button type="submit" className="btn-2d-3d">Start Simulation</button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Run2D_form;