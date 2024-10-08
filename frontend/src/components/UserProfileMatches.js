import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './UserProfileMatches.css'; // Import the CSS file for styling

function UserProfileMatches() {
  const [matches, setMatches] = useState([]);
  const [userProfile, setUserProfile] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true); // Add loading state
  const { id } = useParams(); // This is the username

  // Fetch user ID and profile from username
  const fetchUserProfile = async (username) => {
    try {
      const response = await axios.get('http://localhost:8000/api/profiles/');
      const profiles = response.data;
      console.log(profiles);
      const userProfile = profiles.find(profile => profile.user === username);
      return userProfile || null;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      return null;
    }
  };

  useEffect(() => {
    const fetchMatches = async () => {
      setLoading(true); // Start loading
      try {
        const userProfile = await fetchUserProfile(id);
        if (userProfile) {
          setUserProfile(userProfile);
          const userId = userProfile.user_id;
          const response = await axios.get(`http://localhost:8000/api/matchmaking/${userId}/`);
          setMatches(response.data);
        } else {
          setError('User profile not found');
        }
      } catch (error) {
        setError('Error fetching matches');
        console.error('Error fetching matches:', error);
      } finally {
        setLoading(false); // Stop loading
      }
    };

    fetchMatches();
  }, [id]);

  return (
    <div className="matches-container">
      <h1>Matches for {id}</h1>
      {error && <p className="error">{error}</p>}
      
      {loading ? (
        <div className="loading-spinner">
          <div className="spinner"></div> {/* Display loading animation */}
        </div>
      ) : (
        <>
          {userProfile && (
            <div className="user-profile-card">
              <h2>Your Requirements</h2>
              <p><strong>Your location:</strong> {userProfile.location}</p>
              <p><strong>Skills you can offer them:</strong> {userProfile.skills_offered.map(skill => skill.name).join(', ')}</p>
              <p><strong>Skills you are looking for:</strong> {userProfile.skills_sought.map(skill => skill.name).join(', ')}</p>
            </div>
          )}
          <br />
          <h2>Your Matches</h2>
          <div className="matches-grid">
            {matches.length > 0 ? (
              matches.map(profile => (
                <div className="match-card" key={profile.user}>
                  <div className="match-header">
                    <h2>{profile.user}</h2>
                  </div>
                  <div className="match-body">
                    <p><strong>Location:</strong> {profile.location}</p>
                    <p><strong>Bio:</strong> {profile.bio}</p>
                  </div>
                  <div className="match-footer">
                    <p><strong>Skills Offered:</strong> {profile.skills_offered.map(skill => skill.name).join(', ')}</p>
                    <p><strong>Skills Sought:</strong> {profile.skills_sought.map(skill => skill.name).join(', ')}</p>
                  </div>
                </div>
              ))
            ) : (
              <p>No matches found</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default UserProfileMatches;
