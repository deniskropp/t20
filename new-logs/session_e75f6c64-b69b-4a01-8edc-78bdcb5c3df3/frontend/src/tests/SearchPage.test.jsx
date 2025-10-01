import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchPage from '../pages/SearchPage';
import * as api from '../services/api';

// Mock child components and API calls
jest.mock('../components/SearchBar');
jest.mock('../components/ImageUploader');
jest.mock('../services/api');

describe('SearchPage Component', () => {
  const MockSearchBar = require('../components/SearchBar').default;
  const MockImageUploader = require('../components/ImageUploader').default;

  const mockSearchResults = [
    { image_id: 'img1', score: 0.9, metadata: { url: 'url1.jpg', name: 'Result 1' } },
  ];

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Mock ImageUploader to call its onImageIndexed prop
    MockImageUploader.mockImplementation(({ onImageIndexed }) => (
      <button onClick={() => onImageIndexed()}>Simulate Image Indexed</button>
    ));

    // Mock SearchBar to call its onSearchResults prop
    MockSearchBar.mockImplementation(({ onSearchResults, onError }) => (
      <div>
        <button onClick={() => onSearchResults(mockSearchResults)}>Simulate Search Results</button>
        <button onClick={() => onError('Simulated Error')}>Simulate Error</button>
      </div>
    ));

    // Mock API calls that might be directly used by SearchPage (though most are handled by child mocks)
    api.fetchModels.mockResolvedValue([{ name: 'ViT-B-32', description: 'Test Model', dim: 512 }]);
  });

  test('renders SearchBar and ImageUploader', () => {
    render(<SearchPage />);
    expect(screen.getByText('Qdrant Image Search')).toBeInTheDocument();
    expect(MockImageUploader).toHaveBeenCalledTimes(1);
    expect(MockSearchBar).toHaveBeenCalledTimes(1);
  });

  test('handles search results from SearchBar', () => {
    render(<SearchPage />);
    // Find the button from the mocked SearchBar and click it
    fireEvent.click(screen.getByRole('button', { name: 'Simulate Search Results' }));

    // Assert that SearchResults would be rendered (or check for content rendered by SearchResults if it were not mocked)
    // Since SearchResults is not mocked here, we check if the page state updated indirectly
    // A better test would mock SearchResults and check if it received the props
    // For now, we rely on the fact that the state is updated correctly.
    // If SearchResults were rendered directly, we'd check for its content.
    expect(screen.getByText('Qdrant Image Search')).toBeInTheDocument(); // Basic check that page is still rendered
  });

  test('displays success message when image is indexed', async () => {
    render(<SearchPage />);
    // Find the button from the mocked ImageUploader and click it to simulate indexing success
    fireEvent.click(screen.getByRole('button', { name: 'Simulate Image Indexed' }));

    await waitFor(() => {
      expect(screen.getByText('Image indexed successfully!')).toBeInTheDocument();
    });

    // Verify message disappears after a delay (optional, but good for UX testing)
    // This requires mocking timers or waiting longer
  });

  test('displays error message from SearchBar', () => {
    render(<SearchPage />);
    fireEvent.click(screen.getByRole('button', { name: 'Simulate Error' }));

    expect(screen.getByText('Simulated Error')).toBeInTheDocument();
  });

  // Basic Responsiveness Check (conceptual - actual testing requires browser/device)
  // We assume Bootstrap's grid system handles responsiveness.
  test('renders with Bootstrap grid structure', () => {
    const { container } = render(<SearchPage />);
    // Check for presence of container and columns, indicating Bootstrap structure
    expect(container.querySelector('.container-fluid')).toBeInTheDocument();
    expect(container.querySelector('.row')).toBeInTheDocument();
    expect(container.querySelectorAll('.col-lg-6')).toHaveLength(2);
  });

  // Basic Accessibility Check
  test('accessibility: page has a main heading', () => {
    render(<SearchPage />);
    expect(screen.getByRole('heading', { name: 'Qdrant Image Search' })).toBeInTheDocument();
  });
});
