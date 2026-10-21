# Frontend - React

React application for GID.

## Setup

Install dependencies:
```bash
cd frontend
npm install
```

## Running

Start the development server:
```bash
npm start
```

The application will open automatically at `http://localhost:3000`

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Runs the test suite

## Features

- Connects to the FastAPI backend
- Displays API status and information
- Link to API documentation

## Configuration

The React app is configured to proxy API requests to `http://localhost:8000` (see `package.json`).
