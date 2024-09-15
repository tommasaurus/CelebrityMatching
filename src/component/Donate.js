import React, { useState, useEffect } from "react";
import { CreditCard, DollarSign, Calendar, Lock } from "lucide-react";
import "./Donate.css";
import Navbar from "./Navbar";

const Donate = ({ navigateTo, location }) => {
  const [formData, setFormData] = useState({
    amount: "",
    cardNumber: "",
    expiryDate: "",
    cvv: "",
    cardholderName: "",
  });

  useEffect(() => {
    const amount = location?.state?.amount || "";
    if (amount) {
      setFormData((prevState) => ({
        ...prevState,
        amount: amount.toString(),
      }));
    }
  }, [location]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Donation submitted:", formData);
    // Here you would typically handle the donation processing
    setFormData({
      amount: "",
      cardNumber: "",
      expiryDate: "",
      cvv: "",
      cardholderName: "",
    });
  };

  return (
    <div className='donate-page'>
      <Navbar navigateTo={navigateTo} />

      <div className='donate-container'>
        <div className='donate-content'>
          <h1 className='donate-title'>Support Our Work</h1>
          <p className='donate-subtitle'>
            Your contribution helps us grow and improve!
          </p>

          <form className='donate-form' onSubmit={handleSubmit}>
            <div className='form-group'>
              <label htmlFor='amount'>Donation Amount</label>
              <div className='input-icon-wrapper'>
                <DollarSign size={20} />
                <input
                  type='number'
                  id='amount'
                  name='amount'
                  value={formData.amount}
                  onChange={handleChange}
                  placeholder='Enter amount'
                  required
                />
              </div>
            </div>

            <div className='form-group'>
              <label htmlFor='cardNumber'>Card Number</label>
              <div className='input-icon-wrapper'>
                <CreditCard size={20} />
                <input
                  type='text'
                  id='cardNumber'
                  name='cardNumber'
                  value={formData.cardNumber}
                  onChange={handleChange}
                  placeholder='1234 5678 9012 3456'
                  required
                />
              </div>
            </div>

            <div className='form-row'>
              <div className='form-group'>
                <label htmlFor='expiryDate'>Expiry Date</label>
                <div className='input-icon-wrapper'>
                  <Calendar size={20} />
                  <input
                    type='text'
                    id='expiryDate'
                    name='expiryDate'
                    value={formData.expiryDate}
                    onChange={handleChange}
                    placeholder='MM/YY'
                    required
                  />
                </div>
              </div>

              <div className='form-group'>
                <label htmlFor='cvv'>CVV</label>
                <div className='input-icon-wrapper'>
                  <Lock size={20} />
                  <input
                    type='text'
                    id='cvv'
                    name='cvv'
                    value={formData.cvv}
                    onChange={handleChange}
                    placeholder='123'
                    required
                  />
                </div>
              </div>
            </div>

            <div className='form-group'>
              <label htmlFor='cardholderName'>Cardholder Name</label>
              <input
                type='text'
                id='cardholderName'
                name='cardholderName'
                value={formData.cardholderName}
                onChange={handleChange}
                placeholder='John Doe'
                required
              />
            </div>

            <button type='submit' className='donate-button'>
              <DollarSign size={20} />
              Donate Now
            </button>
          </form>

          <div className='secure-notice'>
            <Lock size={16} />
            <span>Your payment is secure and encrypted</span>
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

export default Donate;
