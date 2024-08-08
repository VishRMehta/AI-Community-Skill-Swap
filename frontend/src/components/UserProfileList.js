import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './UserProfileList.css'; // Import the CSS file for styling

function UserProfileList() {
  const [profiles, setProfiles] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/api/profiles/')  // Ensure the URL is correct
      .then(response => {
        setProfiles(response.data);
      })
      .catch(error => {
        console.error('Error fetching profiles:', error);
        setError('Error fetching profiles.');
      });
  }, []);

  return (
    <div className="profile-container">
      <header className="site-header">
        <div className="brand-logo">
          <img src="/path/to/logo.png" alt="SkillLink Logo" />
        </div>
        <nav className="main-nav">
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </nav>
      </header>

      <main>
        <h1 className="main-heading">Explore User Profiles</h1>
        {error && <p className="error">{error}</p>}
        <div className="profile-grid">
          {profiles.length ? (
            profiles.map(profile => (
              <div className="profile-card" key={profile.user}>
                <Link to={`/profiles/${profile.user}/matches`} className="profile-link">
                  <div className="profile-header">
                    <h2>{profile.user}</h2>
                  </div>
                  <div className="profile-body">
                    <p><strong>Location:</strong> {profile.location}</p>
                    <p><strong>Bio:</strong> {profile.bio}</p>
                  </div>
                  <div className="profile-footer">
                    <p><strong>Skills Offered:</strong> {profile.skills_offered.map(skill => skill.name).join(', ')}</p>
                    <p><strong>Skills Sought:</strong> {profile.skills_sought.map(skill => skill.name).join(', ')}</p>
                  </div>
                </Link>
              </div>
            ))
          ) : (
            <p>No profiles available.</p>
          )}
        </div>
      </main>

      <footer className="site-footer">
        <p>© 2024 SkillLink. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default UserProfileList;
