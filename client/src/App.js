import React, { useState } from "react";
import "./App.css";
import Hero from "./component/hero/Hero";
import Contact from "./component/contact/Contact";
import Donate from "./component/donate/Donate";
import InfiniteScrollImages from "./component/scroll/Scroll";

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
      {currentPage === "scroll" && <InfiniteScrollImages navigateTo={navigateTo} />}
    </div>
  );
}

export default App;
