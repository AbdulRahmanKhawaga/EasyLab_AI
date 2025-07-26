# ML API - CBC Diagnosis

A FastAPI-based machine learning API for CBC (Complete Blood Count) diagnosis.

## Features

- FastAPI REST API
- Machine learning model for CBC diagnosis
- CORS enabled for frontend integration
- Deployed on Railway

## API Endpoints

### Health Check
- `GET /` - Check if the API is running

### Diagnosis
- `POST /api/diagnose` - Get CBC diagnosis

#### Request Body:
```json
{
  "hgb": 14.5,
  "mcv": 90.0,
  "mchc": 34.0,
  "wbc": 7.5,
  "rbc": 4.8,
  "platelets": 250.0,
  "hct": 42.0,
  "mch": 30.0
}
```

#### Response:
```json
{
  "diagnosis": "Normal",
  "confidence": 0.95
}
```

## Deployment

This application is deployed on Railway. The deployment process is automated through Railway's Git integration.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app:app --reload
```

3. Access the API at `http://localhost:8000` 