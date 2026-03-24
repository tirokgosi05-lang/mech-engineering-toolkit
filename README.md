# Mechanical Engineering Toolkit

A full-stack toolkit for quick mechanics calculations with a Flask API + browser UI.

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
flask --app backend.app run --debug
```

Then open:
- Local machine: `http://127.0.0.1:5000`
- If running in Docker/VM/remote dev environment: run with host binding and use forwarded port:
  ```bash
  flask --app backend.app run --debug --host 0.0.0.0 --port 5000
  ```

## Troubleshooting access issues
If you **cannot access the web page**:
1. Confirm Flask is running and shows `Running on ...:5000` in terminal.
2. If you are not on the same machine as the server, use `--host 0.0.0.0` and ensure port `5000` is exposed/forwarded.
3. Test API reachability from terminal:
   ```bash
   curl http://127.0.0.1:5000/api/health
   ```
   Expected response:
   ```json
   {"status":"ok"}
   ```

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
