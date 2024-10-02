import React from "react";
import { Send } from "lucide-react";
import "./Contact.css";
import useContactForm from "./useContactForm.js";

const Contact = () => {
  const {
    formData,
    handleChange,
    handleSubmit,
    isSubmitted,
    submitError,
    isSending,
  } = useContactForm();

  return (
    <div className='contact-page'>
      <div className='contact-content'>
        <h1 className='contact-title'>Contact</h1>
        <p className='contact-subtitle'>We'd love to hear from you!</p>
        <form className='contact-form' onSubmit={handleSubmit}>
          <input
            type='email'
            name='email'
            value={formData.email}
            onChange={handleChange}
            required
            className='form-input'
            placeholder='Email'
          />
          <textarea
            name='message'
            value={formData.message}
            onChange={handleChange}
            required
            className='form-input'
            placeholder='Message'
            rows='4'
          />
          <button type='submit' className='submit-button' disabled={isSending}>
            <Send size={20} />
            {isSending ? "Sending..." : "Send Message"}
          </button>
          <div className='message-container'>
            {isSubmitted && (
              <div className='success-message'>
                Thank you! Your message has been sent.
              </div>
            )}
            {submitError && <div className='error-message'>{submitError}</div>}
          </div>
        </form>
      </div>
    </div>
  );
};

export default Contact;
