import React, { useState, useEffect, useRef } from 'react';
import { Form, Button, Dropdown, Alert } from 'react-bootstrap';
import * as api from '../services/api';

function SearchBar({ onSearchResults, onError }) {
  const [query, setQuery] = useState('');
  const [selectedModel, setSelectedModel] = useState(null);
  const [models, setModels] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);

  const dropdownRef = useRef(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await api.fetchModels();
        setModels(data);
        // Set default model if available
        if (data.length > 0) {
          setSelectedModel(data[0]);
        }
      } catch (err) {
        console.error("Failed to fetch models:", err);
        setError('Failed to load models. Please try again later.');
        setShowError(true);
      }
    };
    fetchModels();
  }, []);

  const handleSearch = async (event) => {
    event.preventDefault();
    if (!query.trim() || !selectedModel) {
      setError('Please enter a search query and select a model.');
      setShowError(true);
      return;
    }

    setIsLoading(true);
    setError(null);
    setShowError(false);

    try {
      const results = await api.searchByText(query, selectedModel.name);
      onSearchResults(results);
    } catch (err) {
      console.error("Search failed:", err);
      const errorMessage = err.message || 'Search failed. Please check your query and try again.';
      setError(errorMessage);
      setShowError(true);
      onError(errorMessage); // Propagate error to parent
      onSearchResults([]); // Clear previous results on error
    } finally {
      setIsLoading(false);
    }
  };

  const handleModelSelect = (model) => {
    setSelectedModel(model);
    // Close dropdown manually after selection if needed, or rely on Bootstrap's behavior
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
        // Close dropdown if it's open and click is outside
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

  const isSearchDisabled = !query.trim() || !selectedModel || isLoading;

  return (
    <Form onSubmit={handleSearch} className="mb-4 d-flex flex-column flex-md-row gap-2 align-items-center">
      <div className="flex-grow-1 w-100">
        <Form.Label htmlFor="search-query" className="visually-hidden">Search Query</Form.Label>
        <Form.Control
          id="search-query"
          type="text"
          placeholder="Enter your search query..."
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            if (showError) {
              setShowError(false); // Hide error when user starts typing again
            }
          }}
          aria-label="Search Query"
          aria-describedby="search-button search-model-button"
          className="w-100"
        />
      </div>

      <Dropdown className="w-100 w-md-auto" ref={dropdownRef}>
        <Dropdown.Toggle id="search-model-button" variant="outline-secondary" className="w-100">
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
        id="search-button"
        type="submit"
        variant="primary"
        disabled={isSearchDisabled}
        aria-label="Search"
      >
        {isLoading ? 'Searching...' : 'Search'}
      </Button>
      {showError && (
        <Alert variant="danger" className="w-100 mt-2" dismissible onClose={() => setShowError(false)}>
          {error}
        </Alert>
      )}
    </Form>
  );
}

export default SearchBar;
