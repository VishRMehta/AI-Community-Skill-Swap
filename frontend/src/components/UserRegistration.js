import React, { useState } from 'react';
import axios from 'axios';
import './UserRegistration.css';

function UserRegistration() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    location: '',
    bio: '',
    skills_offered: '',
    skills_sought: '',
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:8000/api/register/', formData)
      .then(response => {
        setMessage('User registered successfully!');
        setFormData({
          username: '',
          email: '',
          password: '',
          location: '',
          bio: '',
          skills_offered: '',
          skills_sought: '',
        });
      })
      .catch(error => {
        setMessage('Failed to register user.');
        console.error('There was an error registering the user!', error);
      });
  };

  return (
    <div className="registration-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" name="username" value={formData.username} onChange={handleChange} required />
        </label>
        <label>
          Email:
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </label>
        <label>
          Password:
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </label>
        <label>
          Location:
          <input type="text" name="location" value={formData.location} onChange={handleChange} required />
        </label>
        <label>
          Bio:
          <textarea name="bio" value={formData.bio} onChange={handleChange}></textarea>
        </label>
        <label>
          Skills Offered (comma-separated):
          <input type="text" name="skills_offered" value={formData.skills_offered} onChange={handleChange} required />
        </label>
        <label>
          Skills Sought (comma-separated):
          <input type="text" name="skills_sought" value={formData.skills_sought} onChange={handleChange} required />
        </label>
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default UserRegistration;
