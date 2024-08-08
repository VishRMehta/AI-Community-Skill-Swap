import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UserProfileList from './components/UserProfileList';
import UserProfileMatches from './components/UserProfileMatches';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserProfileList />} />
        <Route path="/profiles/:id/matches" element={<UserProfileMatches />} />
      </Routes>
    </Router>
  );
}

export default App;
