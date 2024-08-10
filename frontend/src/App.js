import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UserProfileList from './components/UserProfileList';
import UserProfileMatches from './components/UserProfileMatches';
import About from './components/About';
import Contact from './components/Contact';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserProfileList />} />
        <Route path="/profiles/:id/matches" element={<UserProfileMatches />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </Router>
  );
}

export default App;
