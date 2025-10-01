import React, { useState, useEffect, useRef } from 'react';
import { Form, Button, Image, Alert, Dropdown } from 'react-bootstrap';
import * as api from '../services/api';

function ImageUploader({ onImageIndexed }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [metadata, setMetadata] = useState({ /* initial empty metadata fields */ });
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [showError, setShowError] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const fileInputRef = useRef(null);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await api.fetchModels();
        setModels(data);
        if (data.length > 0) {
          setSelectedModel(data[0]);
        }
      } catch (err) {
        console.error("Failed to fetch models:", err);
        setErrorMessage('Failed to load models. Please try again later.');
        setShowError(true);
      }
    };
    fetchModels();
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        setErrorMessage('Invalid file type. Please select an image.');
        setShowError(true);
        setSelectedFile(null);
        setPreviewUrl('');
        return;
      }
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
        if (showError) {
          setShowError(false); // Clear error if user selects a new file
        }
      };
      reader.onerror = () => {
        console.error("File read error:", reader.error);
        setErrorMessage('Error reading file.');
        setShowError(true);
        setSelectedFile(null);
        setPreviewUrl('');
      };
      reader.readAsDataURL(file);
      setSuccessMessage(''); // Clear previous success message
      setShowSuccess(false);
    }
  };

  const handleMetadataChange = (key, value) => {
    setMetadata(prev => ({ ...prev, [key]: value }));
  };

  const handleAddMetadataField = () => {
    // This is a placeholder. In a real app, you'd have input fields for keys and values.
    // For now, let's assume metadata is handled externally or via a simple structure.
    console.log("Add metadata field called");
  };

  const handleIndexImage = async (event) => {
    event.preventDefault();
    if (!selectedFile || !selectedModel) {
      setErrorMessage('Please select an image and choose a model.');
      setShowError(true);
      return;
    }

    setIsLoading(true);
    setErrorMessage('');
    setShowError(false);
    setSuccessMessage('');
    setShowSuccess(false);

    try {
      // Extract base64 string from previewUrl
      const base64Image = previewUrl.split(',')[1];
      const response = await api.indexImage(base64Image, metadata, selectedModel.name);
      setSuccessMessage('Image indexed successfully!');
      setShowSuccess(true);
      onImageIndexed(response.image_id);
      // Optionally clear form after successful indexing
      setSelectedFile(null);
      setPreviewUrl('');
      setMetadata({});
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (err) {
      console.error("Image indexing failed:", err);
      const errorMessage = err.message || 'Image indexing failed. Please try again.';
      setErrorMessage(errorMessage);
      setShowError(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleModelSelect = (model) => {
    setSelectedModel(model);
    // Close dropdown
    if (dropdownRef.current) {
      dropdownRef.current.classList.remove('show');
      const menu = dropdownRef.current.querySelector('.dropdown-menu');
      if (menu) menu.classList.remove('show');
    }
  };

  // Handle closing dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        const menu = dropdownRef.current.querySelector('.dropdown-menu.show');
        if (menu) {
          dropdownRef.current.classList.remove('show');
          menu.classList.remove('show');
        }
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const isIndexButtonDisabled = !selectedFile || !selectedModel || isLoading;

  return (
    <div className="card mb-4">
      <div className="card-body">
        <h5 className="card-title">Index New Image</h5>
        <Form onSubmit={handleIndexImage}>
          <Form.Group className="mb-3">
            <Form.Label htmlFor="image-upload-input">Choose Image</Form.Label>
            <Form.Control
              id="image-upload-input"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              ref={fileInputRef}
              aria-label="Choose Image file to upload"
            />
          </Form.Group>

          {previewUrl && (
            <div className="mb-3 text-center">
              <Image src={previewUrl} alt="Preview" style={{ maxWidth: '200px', maxHeight: '200px' }} rounded />
            </div>
          )}

          {/* Simple Metadata Input Example */}
          <div className="mb-3 d-flex gap-2">
            <Form.Control
              type="text"
              placeholder="Metadata Key (e.g., url)"
              value={metadata.key || ''}
              onChange={(e) => handleMetadataChange('key', e.target.value)}
              aria-label="Metadata Key Input"
            />
            <Form.Control
              type="text"
              placeholder="Metadata Value"
              value={metadata.value || ''}
              onChange={(e) => handleMetadataChange('value', e.target.value)}
              aria-label="Metadata Value Input"
            />
            <Button variant="secondary" onClick={handleAddMetadataField} disabled={!metadata.key || !metadata.value}>
              Add
            </Button>
          </div>
          {/* Display added metadata (example) */}
          {Object.keys(metadata).length > 2 && (
            <div className="mb-3">
              <h6>Added Metadata:</h6>
              <ul>
                {Object.entries(metadata).map(([key, val]) => (
                  <li key={key}>{key}: {val}</li>
                ))}
              </ul>
            </div>
          )}

          <Dropdown className="mb-3 w-100" ref={dropdownRef}>
            <Dropdown.Toggle variant="outline-secondary" className="w-100">
              {selectedModel ? `${selectedModel.name} (${selectedModel.description})` : 'Select Model'}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {models.map((model) => (
                <Dropdown.Item
                  key={model.name}
                  onClick={() => handleModelSelect(model)}
                  active={selectedModel?.name === model.name}
                  href="#"
                  role="option"
                  aria-selected={selectedModel?.name === model.name}
                >
                  {`${model.name} (${model.description})`}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>

          <Button
            type="submit"
            variant="primary"
            disabled={isIndexButtonDisabled}
            aria-label="Index Image"
          >
            {isLoading ? 'Indexing...' : 'Index Image'}
          </Button>
        </Form>

        {showSuccess && (
          <Alert variant="success" className="mt-3">
            {successMessage}
          </Alert>
        )}
        {showError && (
          <Alert variant="danger" className="mt-3" dismissible onClose={() => setShowError(false)}>
            {errorMessage}
          </Alert>
        )}
      </div>
    </div>
  );
}

export default ImageUploader;
