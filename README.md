# Mechanical Engineering Toolkit

A polished full-stack toolkit for quick mechanics calculations with a Flask API + browser UI.

## Features
- Interactive UI for choosing formulas and entering values.
- Robust backend validation with clear error messages.
- API metadata endpoint for frontend auto-configuration.
- Engineering calculators:
  - Stress (`σ = F / A`)
  - Strain (`ε = ΔL / L₀`)
  - Young's Modulus (`E = σ / ε`)
  - Factor of Safety (`FoS = S / σ_working`)
- Automated tests for main API behavior.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python backend/app.py
```

Open http://127.0.0.1:5000.

## API endpoints
- `GET /api` — API and calculator metadata.
- `GET /api/health` — health check.
- `POST /api/stress`
- `POST /api/strain`
- `POST /api/youngs_modulus`
- `POST /api/safety_factor`

### Sample request
```bash
curl -X POST http://127.0.0.1:5000/api/stress \
  -H "Content-Type: application/json" \
  -d '{"force": 5000, "area": 0.02}'
```

## Running tests

```bash
pytest -q
```
