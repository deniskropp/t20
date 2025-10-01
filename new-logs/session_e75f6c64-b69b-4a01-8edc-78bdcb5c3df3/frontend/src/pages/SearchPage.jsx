import React, { useState } from 'react';
import { Container, Row, Col, Alert } from 'react-bootstrap';
import SearchBar from '../components/SearchBar';
import ImageUploader from '../components/ImageUploader';
import SearchResults from '../components/SearchResults';

function SearchPage() {
  const [searchResults, setSearchResults] = useState([]);
  const [indexingSuccess, setIndexingSuccess] = useState('');
  const [error, setError] = useState('');

  const handleSearchResults = (results) => {
    setSearchResults(results);
    setIndexingSuccess(''); // Clear indexing success message when new search results appear
    setError(''); // Clear any previous errors
  };

  const handleImageIndexed = (imageId) => {
    setIndexingSuccess(`Image indexed successfully! (ID: ${imageId})`);
    setSearchResults([]); // Clear search results after indexing
    setError('');
    // Optionally, auto-hide the success message after a few seconds
    setTimeout(() => setIndexingSuccess(''), 5000);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setIndexingSuccess(''); // Clear indexing success message on error
    setSearchResults([]); // Clear search results on error
  };

  return (
    <Container fluid className="p-3">
      <header className="mb-4 text-center">
        <h1 className="display-5">Qdrant Image Search</h1>
        <p className="text-muted">Search images using text or upload your own.</p>
      </header>

      <Row>
        <Col lg={6} className="mb-4 mb-lg-0">
          <SearchBar onSearchResults={handleSearchResults} onError={handleError} />
          {searchResults.length > 0 && <SearchResults results={searchResults} />}
        </Col>
        <Col lg={6}>
          <ImageUploader onImageIndexed={handleImageIndexed} onError={handleError} />
        </Col>
      </Row>

      {indexingSuccess && (
        <Alert variant="success" className="mt-3" dismissible onClose={() => setIndexingSuccess('')}>
          {indexingSuccess}
        </Alert>
      )}
      {error && (
        <Alert variant="danger" className="mt-3" dismissible onClose={() => setError('')}>
          {error}
        </Alert>
      )}
    </Container>
  );
}

export default SearchPage;
