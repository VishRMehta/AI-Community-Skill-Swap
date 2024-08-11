import React from 'react';
import { Link } from 'react-router-dom';
import './About.css'; // Import the CSS file for styling
import logo from './Logo.png'; // Import the logo image

function About() {
  return (
    <div className="about-container">
      <header className="site-header">
        <div className="brand-logo">
          <img src={logo} alt="SkillLink Logo" />
        </div>
        <nav className="main-nav">
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/about">About</Link></li>
            <li><Link to="/contact">Contact</Link></li>
            <li><a href="/register">Register</a></li>
          </ul>
        </nav>
      </header>

      <main>
        <h1 className="about-heading">About SkillLink</h1>
        <section className="about-content">
          <p>
            Welcome to <strong>SkillLink</strong>, a platform dedicated to connecting people with complementary skills. Our mission is to create a community where users can easily find others to swap knowledge and expertise, fostering a culture of mutual learning and collaboration.
          </p>
          <p>
            Whether you're a seasoned professional looking to share your skills or someone eager to learn something new, SkillLink is the perfect place to find your match. Our advanced matchmaking algorithm ensures that you connect with users who share your interests, goals, and are located near you.
          </p>
          <p>
            At SkillLink, we believe that everyone has something valuable to offer. By connecting individuals with complementary skills, we aim to empower our users to grow, learn, and achieve their personal and professional goals.
          </p>
          <p>
            Join our community today and start making meaningful connections!
          </p>
        </section>
      </main>

      <footer className="site-footer">
        <p>© 2024 SkillLink. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default About;
