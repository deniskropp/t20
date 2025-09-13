## 3D API: Terminology and Vocabulary

This document defines the core terminology and vocabulary for the 3D API domain, consolidating concepts from requirements and the conceptual model. This glossary serves as a reference for consistent communication and development within the project.

### Core Concepts & Entities

*   **Asset:** A fundamental, addressable resource within the 3D API ecosystem. Assets can be models, textures, materials, animations, or other related data. Each asset has a unique identifier.
    *   *Context:* Represents individual components that can be uploaded, stored, and referenced.

*   **Model:** A specific type of Asset that defines 3D geometry. It includes mesh data (vertices, faces, normals, UVs) and can represent a single object or a hierarchical scene structure.
    *   *Context:* Loaded and manipulated by the Geometry Service; forms the visual representation of objects.

*   **Texture:** A specific type of Asset representing image data used to define surface appearance (e.g., color, roughness, normal maps).
    *   *Context:* Applied to Materials; enhances the visual detail of Models.

*   **Material:** Defines the surface properties of a 3D object, dictating how light interacts with it. Materials reference Textures and define shader parameters.
    *   *Context:* Used by the Rendering Service to determine the visual appearance of Models.

*   **Scene:** An organized collection of 3D objects (Models), lights, cameras, and their hierarchical relationships, defining a virtual environment.
    *   *Context:* Managed by the Scene Management Service; the primary context for rendering.

*   **SceneNode:** An element within a Scene's hierarchy. Each SceneNode has a transformation (position, rotation, scale) and can reference a Model, materials, or contain child SceneNodes.
    *   *Context:* Enables hierarchical organization and transformations within a Scene.

*   **Camera:** Defines the viewpoint from which a Scene is rendered. Specifies projection type, field of view, and clipping planes.
    *   *Context:* Configured within a Scene or RenderConfiguration; used by the Rendering Service.

*   **Light:** Defines a light source within a Scene (e.g., directional, point, spot). Specifies type, color, and intensity.
    *   *Context:* Adds illumination to a Scene; affects how Models appear when rendered.

*   **Animation:** Represents time-based changes to properties of SceneNodes or other elements (e.g., skeletal animation, morph targets).
    *   *Context:* Managed by the Animation Service; provides dynamic visual changes.

*   **RenderJob:** Represents a request to generate a 2D image or sequence from a 3D Scene using specified configurations.
    *   *Context:* Handled by the Rendering Service, often asynchronously; produces output assets.

### Core Abstractions & Data Types

*   **`AssetIdentifier`:** A unique identifier used to reference any type of Asset within the API.
    *   *Purpose:* Provides a consistent way to refer to assets regardless of their type or storage location.

*   **`ModelResource`:** An object representing a loaded 3D model, exposing its geometry, scene graph, and metadata.
    *   *Purpose:* Encapsulates model data for manipulation and rendering.

*   **`MaterialDefinition`:** A data structure defining the parameters and texture references for a specific material.
    *   *Purpose:* Allows for the creation and modification of surface appearances.

*   **`SceneDescription`:** A structured representation of a Scene, including its nodes, lights, cameras, and environment settings.
    *   *Purpose:* Defines the complete state of a virtual environment.

*   **`SceneNode` (Abstraction):** A representation of a node within the scene graph, including its transformation and child/model references.
    *   *Purpose:* Facilitates hierarchical scene construction and manipulation.

*   **`RenderConfiguration`:** Specifies all necessary parameters for a rendering operation, including camera settings, output format, and resolution.
    *   *Purpose:* Controls the output and quality of rendered images.

*   **`RenderJobStatus`:** An enumeration indicating the current state of an asynchronous RenderJob (e.g., `QUEUED`, `PROCESSING`, `COMPLETED`, `FAILED`).
    *   *Purpose:* Allows clients to track the progress of background tasks.

*   **`AnimationData`:** A structure containing keyframes and track information for a specific animation.
    *   *Purpose:* Manages animation playback and manipulation data.

### Services & Functionality

*   **Geometry Service:** Handles loading, parsing, validation, and manipulation of 3D model data.
    *   *Key Operations:* Load Model, Parse Geometry, Validate Mesh, Transform Model, Merge Meshes.

*   **Scene Management Service:** Manages the creation, organization, and manipulation of 3D Scenes and their hierarchical structures (SceneNodes).
    *   *Key Operations:* Create Scene, Add/Remove Node, Set Parent, Attach Model, Define Camera/Light.

*   **Rendering Service:** Generates 2D representations (images, frames) from 3D Scenes based on camera and lighting configurations.
    *   *Key Operations:* Render Scene, Configure Renderer, Generate Image.

*   **Material & Texture Service:** Manages the definition, application, and loading of materials and textures.
    *   *Key Operations:* Create Material, Apply Texture, Update Material Properties.

*   **Animation Service:** Supports the definition, playback, and manipulation of animations.
    *   *Key Operations:* Load Animation, Play Animation, Update Animation State.

*   **API Gateway:** The primary entry point for all client interactions, handling request routing, authentication, and rate limiting.
    *   *Key Operations:* Authenticate Request, Route Request, Apply Rate Limits.

*   **Asset Storage:** The system component responsible for the upload, storage, and retrieval of 3D assets.
    *   *Key Operations:* Upload Asset, Download Asset, List Assets.

*   **Database:** Stores metadata related to assets, scenes, users, and API usage.
    *   *Purpose:* Persistence and retrieval of descriptive information.

### Non-Functional Attributes

*   **Latency:** The time delay for API operations.
*   **Scalability:** The ability of the API to handle increasing load.
*   **Availability:** The percentage of time the API is operational.
*   **Extensibility:** The ease with which new features or formats can be added.
*   **Interoperability:** The ability to integrate with other systems and standards.
*   **Security:** Measures taken to protect data and access.
*   **Usability:** The ease with which developers can use the API.
*   **Maintainability:** The ease with which the API can be modified and debugged.