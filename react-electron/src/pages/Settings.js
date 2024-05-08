import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Settings.css';
import { FaPencilAlt } from 'react-icons/fa'; 

const Settings = () => {

    const [user, setUser] = useState({
        username: '',
        email: '',
    });
    const [isEditing, setIsEditing] = useState(false);
    const [newUserData, setNewUserData] = useState({
        username: '',
        email: '',
    });
    
    useEffect(() => {
        const fetchUser = async () => {
        try {
            const response = await axios.get('http://localhost:5000/user', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
            });
            setUser(response.data);
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
        };
    
        fetchUser();
    }, []);
    
    const toggleEdit = () => {
        setIsEditing(!isEditing);
        // Reset newUserData
        setNewUserData({
        username: user.username,
        email: user.email,
        });
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
    
        try {
        const response = await axios.put('http://localhost:5000/user', {
            username: newUserData.username,
            email: newUserData.email,
        }, {
            headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
        });
    
        console.log('User updated successfully:', response.data);
        setUser(newUserData);
        setIsEditing(false);
        } catch (error) {
        console.error('Error updating user:', error);
        }
    };
    
    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewUserData(prevData => ({
        ...prevData,
        [name]: value,
        }));
    };

/*   const getUserName = () => {
    localStorage.getItem('username');
    console.log(localStorage.getItem('username'));
    return localStorage.getItem('username') || 'Login';
  };

  const getMail = () => {
    localStorage.getItem('email');
    console.log(localStorage.getItem('email'));
    return localStorage.getItem('email') || 'Email';
  }
 */
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <div>
            <h2>Settings</h2>
            {!isEditing? (
            <div className="profile-info" style={{ marginBottom: '10px' }}>
                <div className="profile-item">
                <span className="profile-label">Username:</span>
                <span className="profile-value">{user.username}</span>
                </div>
                <div className="profile-item">
                <span className="profile-label">Email:</span>
                <span className="profile-value">{user.email}</span>
                </div>
                <FaPencilAlt className="edit-icon" onClick={toggleEdit} />
            </div>
            ) : (
            <form className="edit-form" onSubmit={handleSubmit}>
                <label className="edit-label">
                Username:
                <input
                    type="text"
                    name="username"
                    value={newUserData.username}
                    onChange={handleChange}
                    className="edit-input"
                />
                </label>
                <label className="edit-label">
                Email:
                <input
                    type="email"
                    name="email"
                    value={newUserData.email}
                    onChange={handleChange}
                    className="edit-input"
                />
                </label>
                <div className="edit-buttons">
                <button type="submit" className="edit-button">Update</button>
                <button type="button" onClick={toggleEdit} className="edit-button">Cancel</button>
                </div>
            </form>
            )}
        </div>
    </div>
  );
};

export default Settings;
