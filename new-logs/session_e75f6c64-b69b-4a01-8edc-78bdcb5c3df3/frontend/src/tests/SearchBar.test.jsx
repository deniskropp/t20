import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchBar from '../components/SearchBar';
import * as api from '../services/api';

// Mock the api functions
jest.mock('../services/api');

describe('SearchBar Component', () => {
  const mockOnSearchResults = jest.fn();
  const mockModels = [
    { name: 'ViT-B-32', description: 'ViT Base 32x32', dim: 512 },
    { name: 'RN50', description: 'ResNet 50', dim: 1024 },
  ];

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    // Mock fetchModels to return mock data
    api.fetchModels.mockResolvedValue(mockModels);
    // Mock searchByText to return empty results by default
    api.searchByText.mockResolvedValue([]);
  });

  test('renders correctly and fetches models on mount', async () => {
    render(<SearchBar onSearchResults={mockOnSearchResults} />);

    // Check if input and button are rendered
    expect(screen.getByPlaceholderText('Enter your search query...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Search' })).toBeInTheDocument();

    // Wait for models to be fetched and dropdown to update
    await waitFor(() => {
      expect(api.fetchModels).toHaveBeenCalledTimes(1);
      expect(screen.getByText('ViT-B-32 (ViT Base 32x32)')).toBeInTheDocument();
    });
  });

  test('allows user to input query and select model', () => {
    render(<SearchBar onSearchResults={mockOnSearchResults} />);

    const queryInput = screen.getByPlaceholderText('Enter your search query...');
    fireEvent.change(queryInput, { target: { value: 'test query' } });
    expect(queryInput).toHaveValue('test query');

    // Click dropdown toggle
    fireEvent.click(screen.getByRole('button', { name: 'Select Model' }));
    // Click on a model item
    fireEvent.click(screen.getByText('RN50 (ResNet 50)'));
    expect(screen.getByRole('button', { name: 'RN50 (ResNet 50)' })).toBeInTheDocument();
  });

  test('calls searchByText API on form submission with valid data', async () => {
    render(<SearchBar onSearchResults={mockOnSearchResults} />);

    // Set initial model
    await waitFor(() => {
        fireEvent.click(screen.getByRole('button', { name: 'Select Model' }));
        fireEvent.click(screen.getByText('ViT-B-32 (ViT Base 32x32)'));
    });

    const queryInput = screen.getByPlaceholderText('Enter your search query...');
    fireEvent.change(queryInput, { target: { value: 'test query' } });

    fireEvent.click(screen.getByRole('button', { name: 'Search' }));

    // Wait for the API call to be made
    await waitFor(() => {
      expect(api.searchByText).toHaveBeenCalledTimes(1);
      expect(api.searchByText).toHaveBeenCalledWith('test query', 'ViT-B-32');
    });

    // Check if onSearchResults was called with the mock results
    expect(mockOnSearchResults).toHaveBeenCalledWith([]); // Initially mocked to return empty array
  });

  test('disables search button and shows error if query is empty', () => {
    render(<SearchBar onSearchResults={mockOnSearchResults} />);
    const searchButton = screen.getByRole('button', { name: 'Search' });
    expect(searchButton).toBeDisabled();

    fireEvent.change(screen.getByPlaceholderText('Enter your search query...'), { target: { value: '' } });
    expect(searchButton).toBeDisabled();

    // Test error message after attempting to submit
    fireEvent.click(screen.getByRole('button', { name: 'Search' }));
    expect(screen.getByText('Please enter a search query and select a model.')).toBeInTheDocument();
  });

  test('handles API error during search', async () => {
    api.searchByText.mockRejectedValue(new Error('API Error'));
    render(<SearchBar onSearchResults={mockOnSearchResults} />);

    // Set initial model
    await waitFor(() => {
        fireEvent.click(screen.getByRole('button', { name: 'Select Model' }));
        fireEvent.click(screen.getByText('ViT-B-32 (ViT Base 32x32)'));
    });

    const queryInput = screen.getByPlaceholderText('Enter your search query...');
    fireEvent.change(queryInput, { target: { value: 'test query' } });

    fireEvent.click(screen.getByRole('button', { name: 'Search' }));

    await waitFor(() => {
      expect(screen.getByText('Search failed. Please check your query and try again.')).toBeInTheDocument();
    });
  });

  test('handles model loading error', async () => {
    api.fetchModels.mockRejectedValue(new Error('Network Error'));
    render(<SearchBar onSearchResults={mockOnSearchResults} />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load models. Please try again later.')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Search' })).toBeDisabled(); // Button should be disabled if no models
    });
  });

  // Accessibility Test
  test('accessibility: input has a label', () => {
    render(<SearchBar onSearchResults={mockOnSearchResults} />);
    const input = screen.getByLabelText('Search Query');
    expect(input).toBeInTheDocument();
  });
});
