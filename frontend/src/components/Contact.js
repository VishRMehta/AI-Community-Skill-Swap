import React from 'react';
import { Link } from 'react-router-dom';
import './Contact.css'; // Import the CSS file for styling
import logo from './Logo.png'; // Import the logo image

function Contact() {
  return (
    <div className="contact-container">
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
        <h1 className="contact-heading">Contact Us</h1>
        <section className="contact-content">
          <p>
            We'd love to hear from you! Whether you have questions, feedback, or just want to say hello, feel free to reach out to us.
          </p>

          <form className="contact-form">
            <div className="form-group">
              <label htmlFor="name">Name:</label>
              <input type="text" id="name" name="name" required />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input type="email" id="email" name="email" required />
            </div>
            <div className="form-group">
              <label htmlFor="message">Message:</label>
              <textarea id="message" name="message" rows="5" required></textarea>
            </div>
            <button type="submit" className="submit-button">Send Message</button>
          </form>
        </section>
      </main>

      <footer className="site-footer">
        <p>© 2024 SkillLink. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Contact;
