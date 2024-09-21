import React, { useState } from "react";
import { Send, Heart } from "lucide-react";
import "./Contact.css";
import { Navbar, Footer } from "../navbar/NavbarFooter";
import "../navbar/NavbarFooter.css";

const Contact = ({ navigateTo }) => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [selectedAmount, setSelectedAmount] = useState(null);
  const [isSending, setIsSending] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError(null);
    setIsSending(true);

    const SCRIPT_URL =
      "https://script.google.com/macros/s/AKfycbwEynB_XHcmCC2e9Kb1w2EVkMx0ZSzEEAyIjf1GFfOBAn3-bgb5sSP8Jm-T2y1aKpWMMw/exec";

    try {
      const url = `${SCRIPT_URL}?nom=${encodeURIComponent(
        formData.name
      )}&email=${encodeURIComponent(
        formData.email
      )}&message=${encodeURIComponent(formData.message)}`;
      const response = await fetch(url, { method: "POST" });
      const data = await response.text();

      if (response.ok) {
        console.log("Form submitted:", formData);
        setFormData({ name: "", email: "", message: "" });
        setIsSubmitted(true);
      } else {
        throw new Error(data || "Failed to send email");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      setSubmitError(
        "There was an error sending your message. Please try again later."
      );
    } finally {
      setIsSending(false);
    }
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
                  <input
                    type='text'
                    id='name'
                    name='name'
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className='form-input'
                    placeholder='Name'
                  />
                </div>
                <div className='form-group'>
                  <input
                    type='email'
                    id='email'
                    name='email'
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className='form-input'
                    placeholder='Email'
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
                  placeholder='Message'
                  rows='4'
                />
              </div>
              {submitError && (
                <div className='error-message'>{submitError}</div>
              )}
              <button
                type='submit'
                className='submit-button'
                disabled={isSending}
              >
                <Send size={20} />
                {isSending ? "Sending..." : "Send Message"}
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
      <Footer navigateTo={navigateTo} /> {/* Add Footer component */}
    </div>
  );
};

export default Contact;
