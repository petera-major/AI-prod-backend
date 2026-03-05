from fastapi import APIRouter
from app.schemas.idea import IdeaInput
from app.schemas.result import ValidationResult, ScoreBreakdown, Competitor
from app.services.pipeline import run_validation_pipeline

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/validate", response_model=ValidationResult)
def validate_idea(body: IdeaInput):
    data = run_validation_pipeline(body)

    return ValidationResult(
        summary=data["summary"],
        scores=ScoreBreakdown(
            viability=data["viability"],
            demand=data["demand"],
            competition=data["competition"],
            differentiation=data["differentiation"],
            monetization_fit=data["monetization_fit"],
            execution_difficulty=data["execution_difficulty"],
            risk=data["risk"],
            confidence=data["confidence"],
        ),
        market_demand=data["market_demand"],
        competitors=[Competitor(**c) for c in data["competitors"]],
        risks=data["risks"],
        monetization=data["monetization"],
        mvp_roadmap=data["mvp_roadmap"],
        next_actions=data["next_actions"],
    )