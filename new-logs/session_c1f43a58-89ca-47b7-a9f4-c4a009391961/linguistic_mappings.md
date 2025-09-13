## Mapping Linguistic Structures to the 3D API Domain

This document outlines the mapping of common linguistic structures and natural language commands to the defined conceptual model and vocabulary of the 3D API. The goal is to facilitate natural language interaction by translating user intentions expressed in language into actionable API operations.

### 1. Core Linguistic Patterns and Corresponding API Mappings

This section identifies common natural language phrases and their corresponding 3D API operations, leveraging the established terminology and abstractions.

**1.1. Asset Management:**

*   **Linguistic Input:** "Upload a model named `my_model.gltf`."
    *   **Intent:** Upload a new asset.
    *   **API Mapping:** `POST /assets` with `asset_type='model'` and file upload (e.g., `my_model.gltf`).
    *   **Key Concepts:** Asset, Model.

*   **Linguistic Input:** "List all available textures."
    *   **Intent:** Retrieve a list of assets of a specific type.
    *   **API Mapping:** `GET /assets?type=texture`.
    *   **Key Concepts:** Asset, Texture.

*   **Linguistic Input:** "Download the material `material_001`."
    *   **Intent:** Retrieve a specific asset.
    *   **API Mapping:** `GET /assets/{material_id}` where `{material_id}` is `material_001`.
    *   **Key Concepts:** Asset, Material.

**1.2. Scene Management:**

*   **Linguistic Input:** "Create a new scene called `my_first_scene`."
    *   **Intent:** Create a new scene.
    *   **API Mapping:** `POST /scenes` with `name='my_first_scene'`.
    *   **Key Concepts:** Scene, `SceneDescription`.

*   **Linguistic Input:** "Add the model `asset_id_xyz` to the scene `scene_id_abc` at position (10, 5, 0)."
    *   **Intent:** Add a model to a scene and specify its transformation.
    *   **API Mapping:** `POST /scenes/{scene_id_abc}/nodes` with request body containing `model_asset_id='asset_id_xyz'` and `transform`.
    *   **Key Concepts:** Scene, SceneNode, Model, `AssetIdentifier`.

*   **Linguistic Input:** "Set the parent of node `node_id_pqr` to `node_id_stu` in scene `scene_id_abc`."
    *   **Intent:** Modify the scene hierarchy.
    *   **API Mapping:** `PATCH /scenes/{scene_id_abc}/nodes/{node_id_pqr}` with `parent_id='node_id_stu'`.
    *   **Key Concepts:** SceneNode.

*   **Linguistic Input:** "Define a camera named `main_cam` in scene `scene_id_abc`."
    *   **Intent:** Add a camera to a scene.
    *   **API Mapping:** `POST /scenes/{scene_id_abc}/cameras` with `name='main_cam'` and camera parameters.
    *   **Key Concepts:** Scene, Camera.

**1.3. Material and Texture Application:**

*   **Linguistic Input:** "Apply material `mat_red` to the model node `node_id_xyz` in scene `scene_id_abc`."
    *   **Intent:** Assign a material to a scene node.
    *   **API Mapping:** `PATCH /scenes/{scene_id_abc}/nodes/{node_id_xyz}` with `material_id='mat_red'`.
    *   **Key Concepts:** SceneNode, Material.

*   **Linguistic Input:** "Create a new PBR material `shiny_metal` with metallic factor 0.9 and roughness 0.2."
    *   **Intent:** Create a new material.
    *   **API Mapping:** `POST /materials` with `name='shiny_metal'`, `shader_type='PBR'`, and parameters.
    *   **Key Concepts:** Material, `MaterialDefinition`.

**1.4. Rendering:**

*   **Linguistic Input:** "Render scene `scene_id_abc` with camera `main_cam` to a PNG image."
    *   **Intent:** Initiate a rendering job.
    *   **API Mapping:** `POST /renderjobs` with `scene_id='scene_id_abc'`, `camera_id='main_cam'`, `output_format='PNG'`.
    *   **Key Concepts:** RenderJob, Scene, Camera, `RenderConfiguration`.

*   **Linguistic Input:** "What is the status of render job `render_job_id_123`?"
    *   **Intent:** Query the status of a render job.
    *   **API Mapping:** `GET /renderjobs/{render_job_id_123}/status`.
    *   **Key Concepts:** RenderJob, `RenderJobStatus`.

**1.5. Animation:**

*   **Linguistic Input:** "Load animation `anim_walk` for node `node_id_abc`."
    *   **Intent:** Attach or load animation data.
    *   **API Mapping:** `POST /animations/attach` with `animation_id='anim_walk'` and `target_node_id='node_id_abc'`.
    *   **Key Concepts:** Animation, SceneNode.

*   **Linguistic Input:** "Play animation `anim_walk` on scene `scene_id_abc`."
    *   **Intent:** Initiate animation playback.
    *   **API Mapping:** `POST /scenes/{scene_id_abc}/play_animation` with `animation_id='anim_walk'`.
    *   **Key Concepts:** Animation, Scene.

### 2. Handling Linguistic Variations and Ambiguity

*   **Synonyms:** Recognize synonyms for common terms (e.g., 'object', 'mesh', 'model' for 'Model'; 'picture', 'image' for 'RenderJob output').
*   **Implicit Information:** Infer missing parameters based on context or defaults (e.g., if no scene is specified for adding a node, assume the currently active or default scene).
*   **Quantifiers:** Handle quantities (e.g., "add three cubes" might involve creating multiple nodes with default cube models).
*   **Action Verbs:** Map various verbs to API operations (e.g., 'create', 'make', 'generate' for POST; 'get', 'show', 'list' for GET; 'change', 'update', 'modify' for PATCH/PUT).
*   **Coreference Resolution:** Understand references like "add *it* to the scene" where "it" refers to a previously mentioned asset or node.

### 3. Mapping to Core Abstractions

*   **`AssetIdentifier`:** Used in commands referring to specific assets (e.g., "use asset `asset_id_123`").
*   **`ModelResource`:** Implicitly loaded when a model asset is added to a scene.
*   **`MaterialDefinition`:** Created or referenced when materials are discussed.
*   **`SceneDescription`:** Manipulated when creating, modifying, or querying scenes.
*   **`SceneNode`:** Directly manipulated when adding objects, transforming them, or setting parent-child relationships.
*   **`RenderConfiguration`:** Specified when requesting renders (e.g., "render in high quality", "render at 1920x1080").
*   **`RenderJobStatus`:** Queried when asking about the progress of a render.
*   **`AnimationData`:** Loaded or applied when animations are mentioned.

This mapping provides a foundational understanding for how natural language inputs can be translated into the structured commands required by the 3D API, enabling more intuitive user interactions.