import React from 'react';

function Footer() {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="bg-light text-center text-lg-start mt-5">
      <div className="text-center p-3" style={{ backgroundColor: '#f8f9fa' }}>
        © {currentYear} Qdrant Service. All rights reserved.
      </div>
    </footer>
  );
}

export default Footer;
