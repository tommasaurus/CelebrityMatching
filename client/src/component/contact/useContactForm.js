import { useState } from "react";

const useContactForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [isSending, setIsSending] = useState(false);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

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

      if (response.ok) {
        setFormData({ name: "", email: "", message: "" });
        setIsSubmitted(true);
        setTimeout(() => setIsSubmitted(false), 5000);
      } else {
        throw new Error((await response.text()) || "Failed to send email");
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

  return {
    formData,
    handleChange,
    handleSubmit,
    isSubmitted,
    submitError,
    isSending,
  };
};

export default useContactForm;
