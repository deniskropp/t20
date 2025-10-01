import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchResults from '../components/SearchResults';

describe('SearchResults Component', () => {
  const mockResults = [
    {
      image_id: 'img1',
      score: 0.95,
      metadata: {
        url: 'http://example.com/img1.jpg',
        name: 'Test Image 1',
        description: 'A beautiful landscape',
        uploaded_by: 'user1',
      },
    },
    {
      image_id: 'img2',
      score: 0.88,
      metadata: {
        name: 'Another Image',
        tags: 'nature, scenic',
      },
    },
  ];

  test('renders correctly with results', () => {
    render(<SearchResults results={mockResults} />);

    expect(screen.getByText('Search Results')).toBeInTheDocument();

    // Check for the first result's details
    expect(screen.getByText('Test Image 1')).toBeInTheDocument();
    expect(screen.getByText('Score: 0.9500')).toBeInTheDocument();
    expect(screen.getByAltText('img1')).toBeInTheDocument();
    expect(screen.getByText('A beautiful landscape')).toBeInTheDocument();
    expect(screen.getByText('Uploaded by: user1')).toBeInTheDocument();

    // Check for the second result's details
    expect(screen.getByText('Another Image')).toBeInTheDocument();
    expect(screen.getByText('Score: 0.8800')).toBeInTheDocument();
    expect(screen.getByText('Tags: nature, scenic')).toBeInTheDocument();
    expect(screen.queryByAltText('img2')).not.toBeInTheDocument(); // No URL for img2
    expect(screen.getByText('Image URL not available')).toBeInTheDocument();
  });

  test('renders nothing when results array is empty', () => {
    render(<SearchResults results={[]} />);
    expect(screen.queryByText('Search Results')).not.toBeInTheDocument();
  });

  test('renders nothing when results prop is null or undefined', () => {
    const { rerender } = render(<SearchResults results={null} />);
    expect(screen.queryByText('Search Results')).not.toBeInTheDocument();

    rerender(<SearchResults results={undefined} />);
    expect(screen.queryByText('Search Results')).not.toBeInTheDocument();
  });

  // Accessibility Test: Ensure images have alt text
  test('accessibility: images have appropriate alt text', () => {
    render(<SearchResults results={mockResults} />);
    expect(screen.getByAltText('img1')).toBeInTheDocument();
    // For the image without a URL, we expect the placeholder text, not an actual image element
    expect(screen.getByText('Image URL not available')).toBeInTheDocument();
  });
});
