from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
CORS(app)


@dataclass(frozen=True)
class Formula:
    name: str
    description: str
    variables: dict[str, str]
    equation: str
    calculator: Callable[[dict[str, float]], float]


def _require_number(payload: dict, key: str, *, positive: bool = True) -> float:
    if key not in payload:
        raise ValueError(f"Missing required field: '{key}'")
    try:
        value = float(payload[key])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Field '{key}' must be a valid number") from exc

    if positive and value <= 0:
        raise ValueError(f"Field '{key}' must be greater than 0")
    return value


def _compute_stress(data: dict[str, float]) -> float:
    force = _require_number(data, "force")
    area = _require_number(data, "area")
    return force / area


def _compute_strain(data: dict[str, float]) -> float:
    delta_length = _require_number(data, "delta_length", positive=False)
    original_length = _require_number(data, "original_length")
    return delta_length / original_length


def _compute_youngs_modulus(data: dict[str, float]) -> float:
    stress = _require_number(data, "stress")
    strain = _require_number(data, "strain", positive=False)
    if strain == 0:
        raise ValueError("Field 'strain' cannot be 0")
    return stress / strain


def _compute_safety_factor(data: dict[str, float]) -> float:
    material_strength = _require_number(data, "material_strength")
    working_stress = _require_number(data, "working_stress")
    return material_strength / working_stress


FORMULAS: dict[str, Formula] = {
    "stress": Formula(
        name="Stress",
        description="Normal stress based on axial force and cross-sectional area.",
        variables={"force": "Applied Force (N)", "area": "Cross-Sectional Area (m²)"},
        equation="σ = F / A",
        calculator=_compute_stress,
    ),
    "strain": Formula(
        name="Strain",
        description="Longitudinal strain from deformation and original length.",
        variables={
            "delta_length": "Change in Length (m)",
            "original_length": "Original Length (m)",
        },
        equation="ε = ΔL / L₀",
        calculator=_compute_strain,
    ),
    "youngs_modulus": Formula(
        name="Young's Modulus",
        description="Elastic modulus from stress and strain in the linear region.",
        variables={"stress": "Stress (Pa)", "strain": "Strain (unitless)"},
        equation="E = σ / ε",
        calculator=_compute_youngs_modulus,
    ),
    "safety_factor": Formula(
        name="Factor of Safety",
        description="Margin against failure under working stress.",
        variables={
            "material_strength": "Material Strength (Pa)",
            "working_stress": "Working Stress (Pa)",
        },
        equation="FoS = S / σ_working",
        calculator=_compute_safety_factor,
    ),
}


@app.get("/")
def home() -> str:
    return render_template("index.html")


@app.get("/api")
def api_info():
    return {
        "message": "Mechanical Engineering Toolkit API",
        "version": "1.0.0",
        "endpoints": {
            f"/api/{key}": {
                "name": formula.name,
                "description": formula.description,
                "equation": formula.equation,
                "variables": formula.variables,
            }
            for key, formula in FORMULAS.items()
        },
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/<operation>")
def calculate(operation: str):
    if operation not in FORMULAS:
        return jsonify({"error": f"Unknown operation '{operation}'"}), 404

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "A JSON payload is required"}), 400

    formula = FORMULAS[operation]
    try:
        result = formula.calculator(payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "operation": operation,
            "name": formula.name,
            "equation": formula.equation,
            "result": result,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
