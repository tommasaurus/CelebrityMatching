import React, { useState } from "react";
import "./App.css";
import Hero from "./component/Hero";
import Contact from "./component/Contact";
import Donate from "./component/Donate";

function App() {
  const [currentPage, setCurrentPage] = useState("home");

  const navigateTo = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className='App'>
      {currentPage === "home" && <Hero navigateTo={navigateTo} />}
      {currentPage === "contact" && <Contact navigateTo={navigateTo} />}
      {currentPage === "donate" && <Donate navigateTo={navigateTo} />}
    </div>
  );
}

export default App;
