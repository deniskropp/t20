import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="text-center">
      <h1>Welcome to the Qdrant Service Frontend</h1>
      <p className="lead">Explore and interact with our powerful image similarity search capabilities.</p>
      <div className="d-flex justify-content-center gap-3 mt-4">
        <Link to="/search" className="btn btn-lg btn-primary">
          Start Searching
        </Link>
        {/* Add more links or call-to-actions as needed */}
      </div>
    </div>
  );
}

export default HomePage;
