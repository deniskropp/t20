## Data Validation Rules and Procedures for the 3D API

This document defines the data validation rules and procedures to ensure the integrity, quality, and consistency of data ingested into the 3D API. These procedures build upon the initial validation performed during upload (T18) and the overall data management plan (T13).

### 1. Validation Stages and Types

Data validation will occur at multiple stages of the ingestion pipeline:

*   **Stage 1: In-Transit Validation (API Endpoint - T18):** Performed immediately upon receiving an asset. Focuses on basic integrity and format.
*   **Stage 2: Pre-Processing Validation (Ingestion Pipeline):** Performed after initial upload but before intensive processing or storage. Ensures data is ready for transformation.
*   **Stage 3: Post-Processing Validation (Ingestion Pipeline):** Performed after data transformation or conversion. Verifies the success and correctness of the processing steps.
*   **Stage 4: Data-at-Rest Validation (Ongoing):** Periodic checks on data already stored to detect corruption or drift.

### 2. Specific Validation Rules

**2.1. File-Level Validation (Stage 1):

*   **File Type:** Check against a predefined list of supported file extensions and MIME types (e.g., `.gltf`, `.glb`, `.obj`, `.fbx`, `.stl`, `.png`, `.jpg`, `.jpeg`). Reject unsupported types.
*   **File Size:** Enforce maximum and minimum file size limits. Reject files that are too large or empty.
*   **Integrity Check:** For certain formats (e.g., compressed archives), perform a basic integrity check (e.g., CRC check if applicable).

**2.2. Metadata Validation (Stage 1 & 2):

*   **Schema Conformance:** Validate all provided metadata against predefined JSON schemas. This ensures expected fields, data types, and formats (e.g., dates, UUIDs, numerical ranges).
*   **Required Fields:** Ensure all mandatory metadata fields are present.
*   **Value Constraints:** Check if metadata values fall within acceptable ranges or adhere to specific formats (e.g., valid enum values, positive integers for counts).
*   **Uniqueness:** For specific fields (e.g., asset IDs, user IDs), ensure uniqueness.

**2.3. 3D Model Content Validation (Stage 2 & 3):

*   **Format Specific Parsing:** Attempt to parse the 3D model file using relevant libraries (e.g., `assimp`, `gltf-transform`). Fail if parsing errors occur.
*   **Geometry Integrity:**
    *   **Manifold Meshes:** Check for non-manifold geometry (e.g., holes, self-intersections) where applicable.
    *   **Valid Normals & UVs:** Ensure normals are consistent and UV coordinates are within expected ranges.
    *   **Vertex/Triangle Count:** Check against reasonable limits to prevent excessively complex models.
*   **Texture Validation:**
    *   **Format & Size:** Verify texture image files are valid and within size limits.
    *   **Color Space:** Ensure textures use appropriate color spaces (e.g., sRGB for albedo, linear for normal maps).
*   **Scene Graph Consistency:** For scene description files, validate hierarchy structure and transformation matrix validity.

**2.4. Data Transformation Validation (Stage 3):

*   **Conversion Success:** Verify that format conversions (e.g., OBJ to glTF) completed without errors.
*   **Output Integrity:** Re-run critical content validation checks on the converted/processed asset to ensure no degradation or corruption occurred.
*   **Metadata Updates:** Ensure any metadata generated or modified during processing is valid.

**2.5. Data-at-Rest Validation (Stage 4):

*   **Checksum Verification:** Periodically re-calculate and verify checksums of stored assets against stored values.
*   **File System Checks:** Run file system integrity checks on storage volumes.
*   **Data Sampling:** Randomly sample stored data and re-run validation checks to detect silent corruption.

### 3. Validation Procedures and Implementation

*   **Automated Checks:** All validation rules (except Stage 4) will be automated as part of the ingestion pipeline.
*   **Schema Management:** A central repository for JSON schemas will be maintained. Tools like `ajv` (for Node.js) or similar libraries will be used for schema validation.
*   **Processing Libraries:** Leverage established libraries for parsing and validating 3D file formats (e.g., `gltf-transform`, `three.js` loaders, `assimp`).
*   **Error Reporting:** Validation failures will be logged with detailed information (file, rule violated, error message). Notifications will be sent for critical failures.
*   **Quarantine/Rejection:** Assets failing Stage 1 or Stage 2 validation may be rejected outright or moved to a quarantine area for manual review. Assets failing Stage 3 validation will trigger rollback or re-processing attempts.
*   **Feedback Loop:** Validation results will feed back into the `Improvement Analyst` (T29) and `Refinement Strategist` (T30) for identifying common issues and improving data quality over time.
*   **Data Validator Role (T19):** This role is responsible for defining, implementing, and maintaining these validation rules and procedures, working closely with `Data Engineer` (T13) and `Ingestion Specialist` (T18).