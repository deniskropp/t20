import React from 'react';

function ResultCard({ result }) {
  // Assuming metadata contains an 'url' or similar field for display
  const imageUrl = result.metadata?.url || `data:image/png;base64,${result.image_base64}` || '/path/to/placeholder.png'; // Fallback if image itself isn't directly available

  return (
    <div className="card mb-3">
      <div className="row g-0">
        <div className="col-md-4">
          {/* Display image if URL is available, otherwise show placeholder or ID */}
          {imageUrl.startsWith('http') ? (
             <img src={imageUrl} className="img-fluid rounded-start" alt={`Result: ${result.image_id}`} style={{ maxWidth: '150px', maxHeight: '150px', objectFit: 'cover' }} />
          ) : (
            <div className="d-flex align-items-center justify-content-center h-100 bg-light text-muted">
              <span>No Image Preview</span>
            </div>
          )}
        </div>
        <div className="col-md-8">
          <div className="card-body">
            <h5 className="card-title">Score: {result.score.toFixed(4)}</h5>
            <p className="card-text"><strong>Image ID:</strong> {result.image_id}</p>
            {Object.entries(result.metadata).map(([key, value]) => (
              <p className="card-text" key={key}><strong>{key}:</strong> {JSON.stringify(value)}</p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
