# Qdrant Service Frontend - Wireframes

These wireframes provide a visual representation of the key user interfaces and flows.

## 1. Home Page (`/`)

```
+----------------------------------------------------+
| Header (Logo, Nav: Home, Models, Index, Search)    |
+----------------------------------------------------+
|                                                    |
|          Welcome to Qdrant Service                 |
|                                                    |
|  [Brief description of the service's capabilities] |
|                                                    |
|  +-----------------+   +-------------------------+ |
|  | Quick Actions:  |   |                         |
|  | - Index Image   |   | [Hero Image/Illustration] |
|  | - Search Images |   |                         |
|  +-----------------+   +-------------------------+ |
|                                                    |
+----------------------------------------------------+
| Footer (Links, Copyright)                          |
+----------------------------------------------------+
```

## 2. Models Page (`/models`)

```
+----------------------------------------------------+
| Header (Logo, Nav: Home, Models, Index, Search)    |
+----------------------------------------------------+
|                                                    |
|                   Available Models                 |
|                                                    |
|  +-----------------------------------------------+ |
|  | Model Name 1                                  | |
|  | Description: [Short description]              | |
|  | Dimensions: [Number]                          | |
|  | [View Details Button (Optional)]              | |
|  +-----------------------------------------------+ |
|  +-----------------------------------------------+ |
|  | Model Name 2                                  | |
|  | Description: [Short description]              | |
|  | Dimensions: [Number]                          | |
|  | [View Details Button (Optional)]              | |
|  +-----------------------------------------------+ |
|  ...                                               |
|                                                    |
+----------------------------------------------------+
| Footer (Links, Copyright)                          |
+----------------------------------------------------+
```

## 3. Index Image Page (`/index`)

```
+----------------------------------------------------+
| Header (Logo, Nav: Home, Models, Index, Search)    |
+----------------------------------------------------+
|                                                    |
|                   Index New Image                  |
|                                                    |
|  +-----------------------------------------------+ |
|  | Drag & Drop or [Browse File] Button           | |
|  |                                               | |
|  | [Image Preview Area]                          | |
|  +-----------------------------------------------+ |
|                                                    |
|  Metadata:                                         |
|  +-----------------------------------------------+ |
|  | Key: [Input Field] Value: [Input Field]       | |
|  | Key: [Input Field] Value: [Input Field]       | |
|  | [Add Metadata Field Button]                   | |
|  +-----------------------------------------------+ |
|                                                    |
|  [Index Image Button]                              |
|                                                    |
+----------------------------------------------------+
| Footer (Links, Copyright)                          |
+----------------------------------------------------+
```

## 4. Search Page (`/search`)

```
+----------------------------------------------------+
| Header (Logo, Nav: Home, Models, Index, Search)    |
+----------------------------------------------------+
|                                                    |
|                       Search                       |
|                                                    |
|  [Tabs: Text Search | Image Search]                |
|                                                    |
|  --- Content for Selected Tab ---                  |
|                                                    |
|  **If Text Search Tab Selected:**                  |
|  +-----------------------------------------------+ |
|  | Query: [Text Input Field]                     | |
|  | Model: [Dropdown: ViT-B-32, RN50, ...]          | |
|  | [Search Button]                               |
|  +-----------------------------------------------+ |
|                                                    |
|  **If Image Search Tab Selected:**                 |
|  +-----------------------------------------------+ |
|  | [Drag & Drop or Browse Image Button]          | |
|  | [Image Preview Area]                          | |
|  | Model: [Dropdown: ViT-B-32, RN50, ...]          | |
|  | [Search Button]                               |
|  +-----------------------------------------------+ |
|                                                    |
|  [Search Results Area - displayed below form]      |
|                                                    |
+----------------------------------------------------+
| Footer (Links, Copyright)                          |
+----------------------------------------------------+
```

## 5. Search Results Display (Common for Text & Image Search)

```
+----------------------------------------------------+
| ... (Search Form Above) ...                        |
+----------------------------------------------------+
|                                                    |
|                    Search Results                  |
|                                                    |
|  +-----------------------------------------------+ |
|  | [Image Thumbnail]                             | |
|  | Image ID: [ID]                                | |
|  | Score: [Score]                                | |
|  | Metadata: [Key: Value, Key: Value]            | |
|  +-----------------------------------------------+ |
|  +-----------------------------------------------+ |
|  | [Image Thumbnail]                             | |
|  | Image ID: [ID]                                | |
|  | Score: [Score]                                | |
|  | Metadata: [Key: Value, Key: Value]            | |
|  +-----------------------------------------------+ |
|  ...                                               |
|                                                    |
+----------------------------------------------------+
```
