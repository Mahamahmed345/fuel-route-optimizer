# Fuel Route Optimizer API

A Django REST API that calculates an optimal driving route between two USA locations, determines fuel stops for a vehicle with a maximum range of 500 miles, and estimates total fuel cost using provided fuel price data.

## Features

- Django REST Framework
- OpenRouteService API
- Fuel optimization
- CSV fuel price lookup
- Reverse geocoding
- Total fuel cost calculation

## Installation

```bash
git clone <repository-url>
cd fuel-route-optimizer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```
ORS_API_KEY=YOUR_API_KEY
```

Run:

```bash
python manage.py runserver
```

API Endpoint

```
POST /api/route/
```

Example Request

```json
{
    "start": "New York, NY",
    "destination": "Chicago, IL"
}
```
