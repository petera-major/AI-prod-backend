from typing import Dict, Any
from app.schemas.idea import IdeaInput
from app.services.llm import generate_analysis_with_llm
from app.services.scorers import compute_viability_score

def run_validation_pipeline(inp: IdeaInput) -> Dict[str, Any]:
    payload = inp.model_dump()

    analysis = generate_analysis_with_llm(payload)

    viability = compute_viability_score(
        demand=analysis["demand"],
        competition=analysis["competition"],
        differentiation=analysis["differentiation"],
        monetization_fit=analysis["monetization_fit"],
        execution_difficulty=analysis["execution_difficulty"],
        risk=analysis["risk"],
    )

    analysis["viability"] = viability
    return analysis