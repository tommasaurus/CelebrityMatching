import React, { useState, useEffect, useRef } from "react";
import { CreditCard, Calendar, Lock, Heart } from "lucide-react";
import ReactConfetti from "react-confetti";
import "./Donate.css";
import { Navbar, Footer } from "../navbar/NavbarFooter";
import "../navbar/NavbarFooter.css";

const DonationInput = ({ value, onChange }) => {
  const [inputValue, setInputValue] = useState(value.toString());
  const inputRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    setInputValue(value.toString());
    if (inputRef.current && containerRef.current) {
      adjustInputWidth();
    }
  }, [value]);

  const formatNumber = (num) => {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  const adjustInputWidth = () => {
    if (inputRef.current && containerRef.current) {
      const textWidth = getTextWidth(inputValue);
      const containerWidth = containerRef.current.offsetWidth;
      const newWidth = Math.max(
        60,
        Math.min(textWidth + 20, containerWidth - 40)
      );
      inputRef.current.style.width = `${newWidth}px`;
    }
  };

  const getTextWidth = (text) => {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    context.font = getComputedStyle(inputRef.current).font;
    return context.measureText(formatNumber(text)).width;
  };

  const handleInputChange = (e) => {
    const newValue = e.target.value.replace(/[^\d]/g, "");
    const numValue = parseInt(newValue, 10);

    if (numValue > 100000) {
      setInputValue("100000");
      onChange(100000);
    } else if (numValue >= 1) {
      setInputValue(newValue);
      onChange(numValue);
    } else {
      setInputValue("");
      onChange(0);
    }

    adjustInputWidth();
  };

  const handleInputBlur = () => {
    if (inputValue === "" || parseInt(inputValue, 10) < 1) {
      setInputValue("5");
      onChange(5);
    }
    adjustInputWidth();
  };

  return (
    <div className='donation-input-wrapper'>
      <span className='donation-label'>Donation Amount</span>
      <div className='input-container' ref={containerRef}>
        <span className='dollar-sign'>$</span>
        <input
          ref={inputRef}
          type='text'
          value={formatNumber(inputValue)}
          onChange={handleInputChange}
          onBlur={handleInputBlur}
          className='donation-input'
        />
      </div>
    </div>
  );
};

const Donate = ({ navigateTo, location }) => {
  const [formData, setFormData] = useState({
    cardNumber: "",
    expiryDate: "",
    cvv: "",
    cardholderName: "",
  });
  const [paymentMethod, setPaymentMethod] = useState("creditCard");
  const [selectedAmount, setSelectedAmount] = useState(5);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);

  const containerRef = useRef(null);

  useEffect(() => {
    const amount = location?.state?.amount || "";
    if (amount) {
      setSelectedAmount(parseInt(amount, 10));
    }
  }, [location]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Donation submitted:", { ...formData, amount: selectedAmount });
    setFormData({
      cardNumber: "",
      expiryDate: "",
      cvv: "",
      cardholderName: "",
    });
    setIsSubmitted(true);
    setShowConfetti(true);
    setTimeout(() => setShowConfetti(false), 5000);
  };

  const handleHotkeyDonation = (amount) => {
    setSelectedAmount(amount);
  };

  return (
    <div className='donate-page' ref={containerRef}>
      <Navbar navigateTo={navigateTo} />
      {showConfetti && (
        <ReactConfetti
          width={containerRef.current?.offsetWidth}
          height={containerRef.current?.offsetHeight}
          gravity={0.3}
          numberOfPieces={200}
        />
      )}
      <div className='donate-container'>
        <div className='donate-content'>
          {isSubmitted ? (
            <div className='submitted-message'>
              <h2>Thank You!</h2>
              <p>
                Your donation of ${selectedAmount} has been successfully
                processed.
              </p>
              <button
                onClick={() => navigateTo("home")}
                className='return-home-button'
              >
                Return to Home
              </button>
            </div>
          ) : (
            <>
              <h1 className='donate-title'>Donate</h1>
              <p className='donate-subtitle'>
                Support our cause with your contribution
              </p>

              <form className='donate-form' onSubmit={handleSubmit}>
                <div className='hotkey-donation-buttons'>
                  {[5, 10, 20, 50].map((amount) => (
                    <button
                      key={amount}
                      type='button'
                      className={`hotkey-donation-button ${
                        selectedAmount === amount ? "active" : ""
                      }`}
                      onClick={() => handleHotkeyDonation(amount)}
                    >
                      ${amount}
                    </button>
                  ))}
                </div>

                <DonationInput
                  value={selectedAmount}
                  onChange={setSelectedAmount}
                />

                <div className='payment-options'>
                  <div
                    className={`payment-option credit-card ${
                      paymentMethod === "creditCard" ? "active" : ""
                    }`}
                    onClick={() => setPaymentMethod("creditCard")}
                  >
                    <CreditCard size={20} style={{ marginRight: "8px" }} />
                    Credit Card
                  </div>
                  <div
                    className={`payment-option apple-pay ${
                      paymentMethod === "applePay" ? "active" : ""
                    }`}
                    onClick={() => setPaymentMethod("applePay")}
                  >
                    <svg
                      xmlns='http://www.w3.org/2000/svg'
                      width='24'
                      height='24'
                      viewBox='0 0 842.32007 1000.0001'
                      className='apple-pay-logo'
                    >
                      <path
                        fill='#fff'
                        d='M824.66636 779.30363c-15.12299 34.93724-33.02368 67.09674-53.7638 96.66374-28.27076 40.3074-51.4182 68.2078-69.25717 83.7012-27.65347 25.4313-57.2822 38.4556-89.00964 39.1963-22.77708 0-50.24539-6.4813-82.21973-19.629-32.07926-13.0861-61.55985-19.5673-88.51583-19.5673-28.27075 0-58.59083 6.4812-91.02193 19.5673-32.48053 13.1477-58.64639 19.9994-78.65196 20.6784-30.42501 1.29623-60.75123-12.0985-91.02193-40.2457-19.32039-16.8514-43.48632-45.7394-72.43607-86.6641-31.060778-43.7024-56.597041-94.37983-76.602609-152.15586C10.740416 658.44309 0 598.01283 0 539.50845c0-67.01648 14.481044-124.8172 43.486336-173.25401C66.28194 327.34823 96.60818 296.6578 134.5638 274.1276c37.95566-22.53016 78.96676-34.01129 123.1321-34.74585 24.16591 0 55.85633 7.47508 95.23784 22.166 39.27042 14.74029 64.48571 22.21538 75.54091 22.21538 8.26518 0 36.27668-8.7405 83.7629-26.16587 44.90607-16.16001 82.80614-22.85118 113.85458-20.21546 84.13326 6.78992 147.34122 39.95559 189.37699 99.70686-75.24463 45.59122-112.46573 109.4473-111.72502 191.36456.67899 63.8067 23.82643 116.90384 69.31888 159.06309 20.61664 19.56727 43.64066 34.69027 69.2571 45.4307-5.55531 16.11062-11.41933 31.54225-17.65372 46.35662zM631.70926 20.0057c0 50.01141-18.27108 96.70693-54.6897 139.92782-43.94932 51.38118-97.10817 81.07162-154.75459 76.38659-.73454-5.99983-1.16045-12.31444-1.16045-18.95003 0-48.01091 20.9006-99.39207 58.01678-141.40314 18.53027-21.27094 42.09746-38.95744 70.67685-53.0663C578.3158 9.00229 605.2903 1.31621 630.65988 0c.74076 6.68575 1.04938 13.37191 1.04938 20.00505z'
                      />
                    </svg>
                    <span>Apple Pay</span>
                  </div>
                </div>

                {paymentMethod === "creditCard" && (
                  <>
                    <div className='form-group'>
                      <label htmlFor='cardholderName'>Name</label>
                      <div className='input-wrapper'>
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
                    </div>

                    <div className='form-group'>
                      <label htmlFor='cardNumber'>Card Number</label>
                      <div className='input-wrapper'>
                        <input
                          type='text'
                          id='cardNumber'
                          name='cardNumber'
                          value={formData.cardNumber}
                          onChange={handleChange}
                          placeholder='1234 5678 9012 3456'
                          required
                        />
                        <CreditCard size={20} className='input-icon' />
                      </div>
                    </div>

                    <div className='form-row'>
                      <div className='form-group'>
                        <label htmlFor='expiryDate'>Expiry</label>
                        <div className='input-wrapper'>
                          <input
                            type='text'
                            id='expiryDate'
                            name='expiryDate'
                            value={formData.expiryDate}
                            onChange={handleChange}
                            placeholder='MM/YY'
                            required
                          />
                          <Calendar size={20} className='input-icon' />
                        </div>
                      </div>

                      <div className='form-group'>
                        <label htmlFor='cvv'>CVV</label>
                        <div className='input-wrapper'>
                          <input
                            type='text'
                            id='cvv'
                            name='cvv'
                            value={formData.cvv}
                            onChange={handleChange}
                            placeholder='123'
                            required
                          />
                          <Lock size={20} className='input-icon' />
                        </div>
                      </div>
                    </div>
                  </>
                )}

                <button type='submit' className='donate-button'>
                  <Heart size={20} />
                  {paymentMethod === "applePay"
                    ? "Donate with Apple Pay"
                    : `Donate $${selectedAmount.toLocaleString()}`}
                </button>
              </form>

              <div className='secure-notice'>
                <Lock size={16} />
                <span>Your payment is secure and encrypted</span>
              </div>
            </>
          )}
        </div>
      </div>
      <Footer navigateTo={navigateTo} /> {/* Add Footer component */}
    </div>
  );
};

export default Donate;
