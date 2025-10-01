# Qdrant Service Frontend

This project provides a frontend interface for interacting with the Qdrant Service.

## Project Setup

### 1. Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── assets/
│   │   └── images/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── SearchBar.jsx
│   │   ├── ImageUploader.jsx
│   │   └── ResultCard.jsx
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   └── SearchPage.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── index.js
│   └── styles/
│       └── main.scss
├── .gitignore
├── package.json
└── README.md
```

-   **`public/`**: Static assets like `index.html`.
-   **`src/`**: Contains all source code.
    -   **`assets/`**: Images, fonts, etc.
    -   **`components/`**: Reusable UI components (e.g., Header, SearchBar).
    -   **`pages/`**: Top-level page components.
    -   **`services/`**: API interaction logic.
    -   **`App.jsx`**: Main application component.
    -   **`index.js`**: Entry point of the application.
    -   **`styles/`**: Global styles and SCSS files.
-   **`.gitignore`**: Specifies intentionally untracked files that Git should ignore.
-   **`package.json`**: Project metadata and dependencies.
