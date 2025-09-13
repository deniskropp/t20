## 3D API: Conceptual Model and Core Abstractions

This document defines the conceptual model and core abstractions for the 3D API, building upon the established architecture and requirements. The goal is to provide a clear, high-level understanding of the fundamental entities and their relationships that the API will manage and expose.

### 1. Conceptual Model

The conceptual model represents the core entities and their interactions within the 3D API domain. It focuses on the 'what' the API deals with, abstracting away implementation details.

**Key Entities:**

*   **Asset:** Represents a fundamental 3D resource. This is a broad category that can encompass models, textures, materials, animations, and potentially other related data.
    *   **Properties:** Unique Identifier, Type (e.g., 'model', 'texture'), File Format, Size, Metadata (e.g., author, creation date, usage rights).
    *   **Relationships:** Can be associated with a Scene, used by a Material, or part of an Animation.

*   **Model:** A specific type of Asset representing 3D geometry. This includes mesh data, vertex information, and potentially scene hierarchy information if it's a composite model.
    *   **Properties:** Geometry Data (vertices, faces, normals, UVs), Bounding Box, File Format (e.g., glTF, OBJ).
    *   **Relationships:** Belongs to an Asset, can be part of a Scene Node.

*   **Texture:** A specific type of Asset representing image data used for surfaces.
    *   **Properties:** Image Data, Dimensions, Format (e.g., PNG, JPG, KTX2), Usage Flags (e.g., diffuse, normal).
    *   **Relationships:** Belongs to an Asset, applied to a Material.

*   **Material:** Defines the surface properties of a 3D object. It dictates how light interacts with the surface.
    *   **Properties:** Shader Type (e.g., PBR, Unlit), Parameters (e.g., albedo color, metallic, roughness, normal map texture reference, occlusion map texture reference).
    *   **Relationships:** Applied to Model(s) or parts of a Model, references Textures.

*   **Scene:** An organized collection of 3D objects, lights, cameras, and other elements that define a virtual environment.
    *   **Properties:** Unique Identifier, Name, Root Node(s), Environment Settings (e.g., background color, skybox).
    *   **Relationships:** Composed of Scene Nodes, may contain multiple Models, Materials, Lights, and Cameras.

*   **SceneNode:** Represents an object within a Scene hierarchy. It defines a transformation (position, rotation, scale) and can contain references to Models, children SceneNodes, or other scene elements.
    *   **Properties:** Transformation Matrix, Name, Parent Node reference, Child Node references, Attached Model reference.
    *   **Relationships:** Part of a Scene, Parent/Child relationships, references Models and Materials.

*   **Camera:** Defines the viewpoint from which a Scene is observed.
    *   **Properties:** Type (Perspective, Orthographic), Field of View / Ortho Size, Aspect Ratio, Near/Far Clipping Planes, Position, Orientation.
    *   **Relationships:** Associated with a Scene.

*   **Light:** Defines a light source within a Scene.
    *   **Properties:** Type (Directional, Point, Spot), Color, Intensity, Position, Direction.
    *   **Relationships:** Associated with a Scene.

*   **Animation:** Represents time-based changes to properties of SceneNodes or other elements.
    *   **Properties:** Type (Skeletal, Morph Target), Duration, Keyframes.
    *   **Relationships:** Can be applied to SceneNodes or Models.

*   **RenderJob:** Represents a request to generate a 2D image or sequence from a Scene.
    *   **Properties:** Unique Identifier, Scene Reference, Camera Configuration, Output Format, Resolution, Status (e.g., PENDING, PROCESSING, COMPLETED, FAILED), Output Location.
    *   **Relationships:** Initiated by a user request, references a Scene, produces output assets.

### 2. Core Abstractions

These are the primary building blocks that API clients will interact with or that represent key data structures within the API. They are derived from the conceptual model and align with the identified services.

**2.1. `AssetIdentifier`:**
*   **Description:** A unique handle to refer to any type of 3D asset (model, texture, material, etc.) stored within the system.
*   **Purpose:** Simplifies referencing assets across different API operations without needing to know the specific asset type or its storage location.
*   **Example Properties:** `asset_id` (UUID), `asset_type` (enum: MODEL, TEXTURE, MATERIAL, ANIMATION).

**2.2. `ModelResource`:**
*   **Description:** Represents a loaded 3D model, providing access to its geometry, hierarchy, and metadata.
*   **Purpose:** Encapsulates model data for manipulation and rendering.
*   **Example Properties:** `asset_id` (AssetIdentifier), `vertex_count`, `triangle_count`, `bounding_box`, `scene_graph_root` (SceneNode).

**2.3. `MaterialDefinition`:**
*   **Description:** Defines the surface properties of a surface.
*   **Purpose:** Allows customization of object appearance.
*   **Example Properties:** `material_id` (unique identifier), `name`, `shader_type`, `parameters` (e.g., `albedo_texture_id`, `metallic_factor`, `roughness_factor`, `emissive_color`).

**2.4. `SceneDescription`:**
*   **Description:** A structured representation of a 3D scene, including its components and their relationships.
*   **Purpose:** Defines the complete setup for rendering or further processing.
*   **Example Properties:** `scene_id` (unique identifier), `name`, `root_nodes` (array of SceneNode), `ambient_light`, `environment_settings`.

**2.5. `SceneNode` (as an abstraction):**
*   **Description:** Represents a node in the scene graph, holding transformations and references to other entities.
*   **Purpose:** Enables hierarchical organization and transformations within a scene.
*   **Example Properties:** `node_id` (unique identifier), `name`, `transform` (matrix or TRS components), `model_asset_id` (optional AssetIdentifier), `children` (array of SceneNode).

**2.6. `RenderConfiguration`:**
*   **Description:** Specifies parameters for a rendering operation.
*   **Purpose:** Controls the output of the rendering service.
*   **Example Properties:** `camera` (Camera definition), `output_format` (e.g., PNG, JPG), `resolution` (width, height), `quality_settings`.

**2.7. `RenderJobStatus`:**
*   **Description:** An enumeration representing the state of an asynchronous rendering task.
*   **Purpose:** Allows clients to track the progress of background operations.
*   **Example Values:** `QUEUED`, `PROCESSING`, `COMPLETED`, `FAILED`.

**2.8. `AnimationData`:**
*   **Description:** Encapsulates animation curves and keyframes.
*   **Purpose:** Manages animation playback and manipulation.
*   **Example Properties:** `animation_id` (AssetIdentifier), `duration`, `tracks` (e.g., `[{ target_node_id, property: 'rotation', keyframes: [...] }]`).

These abstractions provide a foundation for defining the API endpoints, data transfer objects (DTOs), and internal data structures, enabling consistent and powerful interaction with 3D data.