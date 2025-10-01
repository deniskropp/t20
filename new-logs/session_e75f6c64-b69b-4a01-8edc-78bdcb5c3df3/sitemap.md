# Qdrant Service Frontend - Sitemap

This sitemap outlines the structure and navigation of the Qdrant Service frontend.

## 1. Home

*   **Description:** Landing page, introduces the service, provides quick access to core functionalities.
*   **URL:** `/`

## 2. Models

*   **Description:** Displays available machine learning models for image analysis and search.
*   **URL:** `/models`
    *   **Sub-page: Model Details (Optional)**
        *   **Description:** Shows detailed information about a specific model.
        *   **URL:** `/models/{model_name}`

## 3. Index Image

*   **Description:** Interface for uploading an image and its associated metadata to the Qdrant index.
*   **URL:** `/index`

## 4. Search

*   **Description:** Central hub for performing searches. Allows users to choose between text or image-based queries.
*   **URL:** `/search`
    *   **Sub-page: Text Search**
        *   **Description:** Form for entering a text query and selecting a model for search.
        *   **URL:** `/search/text`
    *   **Sub-page: Image Search**
        *   **Description:** Interface for uploading an image and selecting a model for search.
        *   **URL:** `/search/image`

## 5. Benchmarks (Optional/Future Scope)

*   **Description:** Interface for running performance benchmarks on different models.
*   **URL:** `/benchmarks`
    *   **Sub-page: Text Benchmark**
        *   **URL:** `/benchmarks/text`
    *   **Sub-page: Image Benchmark**
        *   **URL:** `/benchmarks/image`

## 6. API Documentation (Link)

*   **Description:** Link to the automatically generated API documentation (e.g., Swagger UI).
*   **URL:** `/docs` (standard FastAPI/Swagger UI path)
