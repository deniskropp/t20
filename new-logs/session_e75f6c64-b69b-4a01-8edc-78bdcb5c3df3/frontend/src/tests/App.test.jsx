import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../App';
import * as api from '../services/api';

// Mock the API service to control responses during tests
jest.mock('../services/api');

describe('App Component (Main Routing and Integration)', () => {
  const mockModels = [
    { name: 'ViT-B-32', description: 'ViT Base 32x32', dim: 512 },
    { name: 'RN50', description: 'ResNet 50', dim: 1024 },
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock fetchModels to be available for components that need it
    api.fetchModels.mockResolvedValue(mockModels);
    // Mock searchByText and indexImage to avoid actual API calls
    api.searchByText.mockResolvedValue([]);
    api.indexImage.mockResolvedValue({ image_id: 'mock-image-id' });
  });

  test('renders the main SearchPage component', () => {
    render(<App />);
    expect(screen.getByText('Qdrant Image Search')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your search query...')).toBeInTheDocument();
    expect(screen.getByText('Choose Image')).toBeInTheDocument();
  });

  test('allows searching for an image using text', async () => {
    render(<App />);

    // Simulate typing into the search bar
    const queryInput = screen.getByPlaceholderText('Enter your search query...');
    fireEvent.change(queryInput, { target: { value: 'a cat' } });

    // Select a model (requires opening dropdown and clicking item)
    fireEvent.click(screen.getByRole('button', { name: 'Select Model' }));
    fireEvent.click(screen.getByText('ViT-B-32 (ViT Base 32x32)'));

    // Simulate form submission
    fireEvent.click(screen.getByRole('button', { name: 'Search' }));

    // Wait for the API call and potentially for results to be displayed
    await waitFor(() => {
      expect(api.searchByText).toHaveBeenCalledTimes(1);
      expect(api.searchByText).toHaveBeenCalledWith('a cat', 'ViT-B-32');
      // If SearchResults were visible, we'd assert its content here.
      // For now, we just check that the API call was made.
    });
  });

  test('allows indexing an image', async () => {
    render(<App />);

    // Mock FileReader for image upload
    const mockFileReaderInstance = {
      readAsDataURL: jest.fn(),
      onerror: null,
      onloadend: jest.fn(),
    };
    global.FileReader = jest.fn(() => mockFileReaderInstance);

    // Simulate file selection
    const fileInput = screen.getByLabelText('Choose Image');
    const mockFile = new File(['image content'], 'test.png', { type: 'image/png' });
    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    // Simulate FileReader onloadend
    const base64Image = 'base64encodedstring';
    mockFileReaderInstance.onloadend.mockImplementation(() => {
      mockFileReaderInstance.result = `data:image/png;base64,${base64Image}`;
    });
    mockFileReaderInstance.readAsDataURL(mockFile);

    // Wait for FileReader simulation and then click Index Image button
    await waitFor(() => {
        expect(mockFileReaderInstance.result).toBeDefined();
    });

    // Select a model for indexing
    fireEvent.click(screen.getByRole('button', { name: 'Select Model' }));
    fireEvent.click(screen.getByText('ViT-B-32 (ViT Base 32x32)'));

    // Click the index button
    fireEvent.click(screen.getByRole('button', { name: 'Index Image' }));

    // Wait for the API call
    await waitFor(() => {
      expect(api.indexImage).toHaveBeenCalledTimes(1);
      expect(api.indexImage).toHaveBeenCalledWith(base64Image, expect.any(Object));
    });

    // Check for success message
    await waitFor(() => {
      expect(screen.getByText('Image indexed successfully!')).toBeInTheDocument();
    });

    // Clean up mock FileReader
    delete global.FileReader;
  });

  // Basic Responsiveness Test: Check if main layout elements are present
  test('responsiveness: uses Bootstrap grid classes', () => {
    const { container } = render(<App />);
    expect(container.querySelector('.container-fluid')).toBeInTheDocument();
    expect(container.querySelector('.row')).toBeInTheDocument();
    expect(container.querySelectorAll('.col-lg-6')).toHaveLength(2); // Based on SearchPage layout
  });

  // Basic Accessibility Test: Check for semantic elements and ARIA attributes
  test('accessibility: has semantic elements and ARIA attributes', () => {
    render(<App />);
    // Check for main heading
    expect(screen.getByRole('heading', { name: 'Qdrant Image Search' })).toBeInTheDocument();
    // Check for form elements with labels
    expect(screen.getByLabelText('Search Query')).toBeInTheDocument();
    expect(screen.getByLabelText('Choose Image')).toBeInTheDocument();
    // Check for buttons with accessible names
    expect(screen.getByRole('button', { name: 'Search' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Index Image' })).toBeInTheDocument();
  });
});
