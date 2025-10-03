# Orbital Viewer Frontend

This is the **frontend** of the Orbital Viewer application, a React-based web interface for visualizing orbital trajectories in 3D. The application uses `three.js` for rendering 3D scenes and integrates with a backend API to fetch orbital data.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Development Server](#running-the-development-server)
  - [Building for Production](#building-for-production)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **3D Orbit Visualization**: Displays orbital trajectories using `three.js`.
- **Dynamic Interaction**: Zoom, pan, and rotate the 3D scene with `OrbitControls`.
- **Dark Theme Support**: Fully styled with a dark theme using CSS variables.
- **Responsive Design**: Adapts to different screen sizes.
- **Error Handling**: Includes an `ErrorBoundary` component for graceful error recovery.

---

## Project Structure

```
frontend/
├── .gitignore          # Files and folders to ignore in Git
├── eslint.config.js    # ESLint configuration for linting
├── index.html          # Main HTML file
├── package.json        # Project metadata and dependencies
├── README.md           # Project documentation
├── vite.config.js      # Vite configuration for development and build
├── public/             # Static assets
│   └── vite.svg        # Vite logo
├── src/                # Source code
│   ├── App.jsx         # Main application component
│   ├── main.jsx        # Entry point for React
│   ├── assets/         # Static assets for the app
│   │   └── react.svg   # React logo
│   ├── components/     # React components
│   │   ├── ErrorBoundary.jsx # Error boundary for catching runtime errors
│   │   ├── OrbitVisualizer.jsx # 3D orbit visualization component
│   │   └── VerticalMenu.jsx   # Vertical menu component
│   ├── css/            # CSS styles
│   │   ├── App.css     # Main application styles
│   │   ├── colors.css  # Theme color variables
│   │   └── index.css   # Global styles
│   ├── services/       # API services
│   │   └── api.js      # Functions for interacting with the backend API
```

---

## Technologies Used

- **React**: JavaScript library for building user interfaces.
- **Three.js**: JavaScript library for 3D rendering.
- **Vite**: Build tool for fast development and production builds.
- **CSS Variables**: For theming and styling.
- **ErrorBoundary**: React component for handling runtime errors gracefully.

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Node.js**: [Download and install Node.js](https://nodejs.org/)
- **npm**: Comes with Node.js (or use `yarn` as an alternative).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/orbital-viewer-frontend.git
   cd orbital-viewer-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Development Server

Start the development server:
```bash
npm start
```

The app will be available at `http://localhost:5173`.

### Building for Production

Build the app for production:
```bash
npm run build
```

The production-ready files will be in the `dist/` directory.

---

## Usage

1. Start the backend server (refer to the backend README for instructions).
2. Open the frontend in your browser.
3. Use the "Load Orbit" button to fetch and visualize orbital data.

---

## Customization

- **Colors**: Modify `src/css/colors.css` to adjust theme colors.
- **API Endpoints**: Update `src/services/api.js` to change the backend API endpoints.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is private and for intended use only