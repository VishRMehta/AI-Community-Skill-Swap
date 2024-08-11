import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './UserProfileList.css'; // Import the CSS file for styling
import logo from './Logo.png'; // Import the logo image

function UserProfileList() {
  const [profiles, setProfiles] = useState([]);
  const [filteredProfiles, setFilteredProfiles] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/api/profiles/')  // Ensure the URL is correct
      .then(response => {
        setProfiles(response.data);
        setFilteredProfiles(response.data); // Initially, show all profiles
      })
      .catch(error => {
        console.error('Error fetching profiles:', error);
        setError('Error fetching profiles.');
      });
  }, []);

  // Filter profiles based on search term
  useEffect(() => {
    const results = profiles.filter(profile => {
      const profileText = `${profile.user} ${profile.location} ${profile.skills_offered.map(skill => skill.name).join(', ')} ${profile.skills_sought.map(skill => skill.name).join(', ')}`.toLowerCase();
      return profileText.includes(searchTerm.toLowerCase());
    });
    setFilteredProfiles(results);
  }, [searchTerm, profiles]);

  return (
    <div className="profile-container">
      <header className="site-header">
        <div className="brand-logo">
          <img src={logo} alt="SkillLink Logo" />
        </div>
        <nav className="main-nav">
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/register">Register</a></li>
          </ul>
        </nav>
      </header>

      <main>
        <h1 className="main-heading">Explore User Profiles</h1>

        <input 
          type="text" 
          className="search-bar" 
          placeholder="Search by name, location, or skills..." 
          value={searchTerm} 
          onChange={(e) => setSearchTerm(e.target.value)} 
        />

        {error && <p className="error">{error}</p>}
        <div className="profile-grid">
          {filteredProfiles.length ? (
            filteredProfiles.map(profile => (
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
