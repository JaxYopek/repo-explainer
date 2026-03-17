# Quick Start Guide

## Backend Setup

1. Install backend dependencies:
```bash
pip install -r requirements-api.txt
```

2. Start the FastAPI server:
```bash
uvicorn backend:app --reload
```

The backend will run on `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install frontend dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000` and automatically open in your browser.

## Running Both

Open two terminals:

**Terminal 1 (Backend):**
```bash
pip install -r requirements-api.txt
uvicorn backend:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm install  # Only needed once
npm run dev
```

Visit `http://localhost:3000` in your browser to use the app.

## For Production

### Backend:
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000
```

### Frontend:
```bash
cd frontend
npm run build
```

This creates a `dist` folder with production-ready files.

## Troubleshooting

- **Port already in use**: Change port with `uvicorn backend:app --port 8001` or `npm run dev -- --port 3001`
- **Module not found**: Make sure you've installed dependencies in the correct directory
- **API requests failing**: Check that the backend is running on `http://localhost:8000`
