import React, { useState } from "react";
import { Send, Heart } from "lucide-react";
import "./Contact.css";
import Navbar from "./Navbar";

const Contact = ({ navigateTo }) => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [selectedAmount, setSelectedAmount] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
    setFormData({ name: "", email: "", message: "" });
    setIsSubmitted(true);
  };

  const handleAmountSelect = (amount) => {
    setSelectedAmount(amount);
  };

  const handleDonation = () => {
    if (selectedAmount) {
      navigateTo("donate", { state: { amount: selectedAmount } });
    }
  };

  return (
    <div className='contact-page'>
      <Navbar navigateTo={navigateTo} />
      <div className='contact-container'>
        <div className='contact-content'>
          <h1 className='contact-title'>Feedback</h1>
          <p className='contact-subtitle'>We'd love to hear from you!</p>
          {isSubmitted ? (
            <div className='success-message'>
              Thank you! Your message has been sent.
            </div>
          ) : (
            <form className='contact-form' onSubmit={handleSubmit}>
              <div className='form-row'>
                <div className='form-group'>
                  <textarea
                    type='text'
                    id='name'
                    name='name'
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className='form-input'
                    placeholder='Name'
                    style={{ maxHeight: "50px" }}
                  />
                </div>
                <div className='form-group'>
                  <textarea
                    type='email'
                    id='email'
                    name='email'
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className='form-input'
                    placeholder='Email'
                    style={{ maxHeight: "50px" }}
                  />
                </div>
              </div>
              <div className='form-group'>
                <textarea
                  id='message'
                  name='message'
                  value={formData.message}
                  onChange={handleChange}
                  required
                  className='form-input'
                  placeholder='message'
                  style={{ minHeight: "120px" }}
                ></textarea>
              </div>
              <button type='submit' className='submit-button'>
                <Send size={20} />
                Send Message
              </button>
            </form>
          )}
          <div className='donate-section'>
            <h2 className='donate-title'>Support Our Cause</h2>
            <p className='donate-subtitle'>We'd love your help!</p>
            <div className='donate-options-grid'>
              {[5, 10, 20, 50].map((amount) => (
                <button
                  key={amount}
                  className={`donate-option ${
                    selectedAmount === amount ? "selected" : ""
                  }`}
                  onClick={() => handleAmountSelect(amount)}
                >
                  ${amount}
                </button>
              ))}
            </div>
            <button className='donate-now-button' onClick={handleDonation}>
              <Heart size={20} />
              Donate Now
            </button>
          </div>
        </div>
      </div>
      <footer className='footer'>
        <div className='footer-content'>
          <p>&copy; 2024 PornTwin. All rights reserved.</p>
          <nav className='footer-nav'>
            <a href='#' onClick={() => navigateTo("contact")}>
              Contact
            </a>
            <a href='#' onClick={() => navigateTo("donate")}>
              Donate
            </a>
          </nav>
        </div>
      </footer>
    </div>
  );
};

export default Contact;
