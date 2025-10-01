import React from 'react';
import { Card, Image, Alert, Row, Col } from 'react-bootstrap';

function SearchResults({ results }) {
  if (!results || results.length === 0) {
    return null; // Don't render anything if there are no results
  }

  return (
    <div className="mt-4">
      <h4>Search Results</h4>
      <Row xs={1} sm={2} md={3} lg={4} className="g-4">
        {results.map((result) => (
          <Col key={result.image_id}>
            <Card className="h-100">
              <Card.Header>
                <Card.Title as="h5">{result.metadata.name || 'Unnamed Image'}</Card.Title>
              </Card.Header>
              <Card.Body>
                {result.metadata.url ? (
                  <Image 
                    src={result.metadata.url} 
                    alt={result.metadata.name || `Image ID: ${result.image_id}`}
                    className="img-fluid mb-2 rounded"
                    aria-label={`Image preview for ${result.metadata.name || result.image_id}`}
                  />
                ) : (
                  <div className="text-muted mb-2">Image URL not available</div>
                )}
                <Card.Text>
                  <strong>Score:</strong> {result.score.toFixed(4)}
                </Card.Text>
                {result.metadata.description && (
                  <Card.Text>
                    <strong>Description:</strong> {result.metadata.description}
                  </Card.Text>
                )}
                {result.metadata.uploaded_by && (
                  <Card.Text>
                    <strong>Uploaded by:</strong> {result.metadata.uploaded_by}
                  </Card.Text>
                )}
                {/* Render other metadata fields dynamically */}
                {Object.entries(result.metadata).map(([key, value]) => {
                  if (!['url', 'name', 'description', 'uploaded_by'].includes(key) && value) {
                    return (
                      <Card.Text key={key}>
                        <strong>{key.charAt(0).toUpperCase() + key.slice(1)}:</strong> {value}
                      </Card.Text>
                    );
                  }
                  return null;
                })}
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}

export default SearchResults;
