import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic validation
    if (!username || !email || !password) {
      setError('All fields are required.');
      return;
    }

    if (!validateEmail(email)) {
      setError('Please enter a valid email address.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/users', {
        username,
        email,
        password
      });
      console.log(response.data);
      navigate('/login');
    } catch (error) {
      console.error(error);
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', padding: '20px', boxSizing: 'border-box' }}>
      <h1 style={{ fontSize: '2em', color: '#007bff', marginBottom: '20px' }}>Register</h1>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
        <input 
          type="text" 
          name="username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
          placeholder="Username" 
          style={{ width: '100%', padding: '10px', margin: '10px 0', boxSizing: 'border-box', border: '1px solid #ccc', borderRadius: '4px' }} 
          required 
        />
        <input 
          type="email" 
          name="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          placeholder="Email" 
          style={{ width: '100%', padding: '10px', margin: '10px 0', boxSizing: 'border-box', border: '1px solid #ccc', borderRadius: '4px' }} 
          required 
        />
        <input 
          type="password" 
          name="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          placeholder="Password" 
          style={{ width: '100%', padding: '10px', margin: '10px 0', boxSizing: 'border-box', border: '1px solid #ccc', borderRadius: '4px' }} 
          required 
        />
        {error && <p style={{ color: 'red', marginBottom: '10px' }}>{error}</p>}
        <button type="submit" style={{ padding: '10px 20px', margin: '10px 0', cursor: 'pointer', border: 'none', borderRadius: '4px', backgroundColor: '#007bff', color: 'white' }}>Register</button>
      </form>
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <Link to="/login" style={{ color: '#007bff', textDecoration: 'none' }}>Already have an account? Login</Link>
      </div>
    </div>
  );
}

export default Register;
