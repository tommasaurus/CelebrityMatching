import React, { useState } from "react";
import "./App.css";
import Hero from "./component/hero/Hero";
import Contact from "./component/contact/Contact";
import Donate from "./component/donate/Donate";
import InfiniteScrollImages from "./component/scroll/Scroll";
import { Navbar, Footer } from "./component/navbar/NavbarFooter";

function App() {
  const [currentPage, setCurrentPage] = useState("home");

  const navigateTo = (page) => {
    setCurrentPage(page);
    window.scrollTo(0, 0);
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case "home":
        return <Hero navigateTo={navigateTo} />;
      case "contact":
        return <Contact />;
      case "donate":
        return <Donate />;
      case "scroll":
        return <InfiniteScrollImages />;
      case "privacy-policy":
        return <div>Privacy Policy Page</div>;
      case "terms-of-service":
        return <div>Terms of Service Page</div>;
      default:
        return <Hero navigateTo={navigateTo} />;
    }
  };

  return (
    <div className='App'>
      <Navbar navigateTo={navigateTo} />
      <main>{renderCurrentPage()}</main>
      <Footer navigateTo={navigateTo} />
    </div>
  );
}

export default App;
