import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ImageUploader from '../components/ImageUploader';
import * as api from '../services/api';

// Mock the api functions
jest.mock('../services/api');

describe('ImageUploader Component', () => {
  const mockOnImageIndexed = jest.fn();
  const mockModels = [
    { name: 'ViT-B-32', description: 'ViT Base 32x32', dim: 512 },
    { name: 'RN50', description: 'ResNet 50', dim: 1024 },
  ];

  // Mock FileReader API
  let mockFileReaderInstance;
  beforeAll(() => {
    mockFileReaderInstance = {
      readAsDataURL: jest.fn(),
      onerror: null,
      onloadend: null,
    };
    global.FileReader = jest.fn(() => mockFileReaderInstance);
  });

  afterAll(() => {
    delete global.FileReader;
  });

  beforeEach(() => {
    jest.clearAllMocks();
    api.fetchModels.mockResolvedValue(mockModels);
    api.indexImage.mockResolvedValue({ image_id: 'test-image-id' });
    // Reset FileReader mock handlers
    mockFileReaderInstance.onerror = null;
    mockFileReaderInstance.onloadend = null;
  });

  test('renders correctly and fetches models', async () => {
    render(<ImageUploader onImageIndexed={mockOnImageIndexed} />);

    expect(screen.getByText('Index New Image')).toBeInTheDocument();
    expect(screen.getByText('Choose Image')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Index Image' })).toBeDisabled(); // Disabled initially

    await waitFor(() => {
      expect(api.fetchModels).toHaveBeenCalledTimes(1);
      expect(screen.getByRole('button', { name: 'Select Model' })).toBeInTheDocument();
      expect(screen.getByText('ViT-B-32 (ViT Base 32x32)')).toBeInTheDocument();
    });
  });

  test('handles file selection and preview', () => {
    render(<ImageUploader onImageIndexed={mockOnImageIndexed} />);
    const fileInput = screen.getByLabelText('Choose Image');
    const mockFile = new File(['(⌐■_■)'], 'test.png', { type: 'image/png' });

    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    // Simulate FileReader onloadend to set previewUrl
    mockFileReaderInstance.onloadend({
      target: {
        result: 'data:image/png;base64,SGVsbG8gV29ybGQ=' // Dummy base64
      }
    });

    expect(screen.getByAltText('Preview')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Index Image' })).not.toBeDisabled();
  });

  test('handles metadata input', () => {
    render(<ImageUploader onImageIndexed={mockOnImageIndexed} />);
    const fileInput = screen.getByLabelText('Choose Image');
    const mockFile = new File(['content'], 'test.png', { type: 'image/png' });
    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    // Simulate FileReader
     mockFileReaderInstance.onloadend({
      target: {
        result: 'data:image/png;base64,SGVsbG8gV29ybGQ='
      }
    });

    // Add custom metadata
    fireEvent.change(screen.getByPlaceholderText('Key'), { target: { value: 'location' } });
    fireEvent.change(screen.getByPlaceholderText('Value'), { target: { value: 'New York' } });
    fireEvent.click(screen.getByRole('button', { name: 'Add' }));

    expect(screen.getByDisplayValue('New York')).toBeInTheDocument();
  });

  test('calls indexImage API on upload and shows success message', async () => {
    render(<ImageUploader onImageIndexed={mockOnImageIndexed} />);
    const fileInput = screen.getByLabelText('Choose Image');
    const mockFile = new File(['content'], 'test.png', { type: 'image/png' });
    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    // Simulate FileReader
    const base64Content = 'mockBase64Content';
    mockFileReaderInstance.onloadend({
      target: {
        result: `data:image/png;base64,${base64Content}`
      }
    });

    // Select a model
    await waitFor(() => {
        fireEvent.click(screen.getByRole('button', { name: 'Select Model' }));
        fireEvent.click(screen.getByText('ViT-B-32 (ViT Base 32x32)'));
    });

    fireEvent.click(screen.getByRole('button', { name: 'Index Image' }));

    // Wait for FileReader to be called and then for API call
    await waitFor(() => {
        expect(mockFileReaderInstance.readAsDataURL).toHaveBeenCalledWith(mockFile);
        expect(api.indexImage).toHaveBeenCalledTimes(1);
        expect(api.indexImage).toHaveBeenCalledWith(base64Content, expect.any(Object)); // Check base64 and metadata object
    });

    await waitFor(() => {
      expect(screen.getByText('Image indexed successfully!')).toBeInTheDocument();
      expect(mockOnImageIndexed).toHaveBeenCalledWith('test-image-id');
    });
  });

  test('handles API error during indexing', async () => {
    api.indexImage.mockRejectedValue(new Error('Indexing Failed'));
    render(<ImageUploader onImageIndexed={mockOnImageIndexed} />);
    const fileInput = screen.getByLabelText('Choose Image');
    const mockFile = new File(['content'], 'test.png', { type: 'image/png' });
    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    mockFileReaderInstance.onloadend({
      target: {
        result: 'data:image/png;base64,SGVsbG8=' 
      }
    });

    await waitFor(() => {
        fireEvent.click(screen.getByRole('button', { name: 'Select Model' }));
        fireEvent.click(screen.getByText('ViT-B-32 (ViT Base 32x32)'));
    });

    fireEvent.click(screen.getByRole('button', { name: 'Index Image' }));

    await waitFor(() => {
      expect(screen.getByText('Image indexing failed. Please try again.')).toBeInTheDocument();
    });
  });

  test('handles FileReader error', async () => {
    render(<ImageUploader onImageIndexed={mockOnImageIndexed} />);
    const fileInput = screen.getByLabelText('Choose Image');
    const mockFile = new File(['content'], 'test.png', { type: 'image/png' });
    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    // Simulate FileReader error
    mockFileReaderInstance.onerror(new Error('File read error'));

    await waitFor(() => {
      expect(screen.getByText('Error reading file.')).toBeInTheDocument();
    });
  });

  // Accessibility Test
  test('accessibility: file input has a label', () => {
    render(<ImageUploader onImageIndexed={mockOnImageIndexed} />);
    const input = screen.getByLabelText('Choose Image');
    expect(input).toBeInTheDocument();
  });
});
