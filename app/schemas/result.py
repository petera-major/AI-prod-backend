from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ScoreBreakdown(BaseModel):
    viability: int = Field(..., ge=0, le=100)
    demand: int = Field(..., ge=0, le=100)
    competition: int = Field(..., ge=0, le=100)
    differentiation: int = Field(..., ge=0, le=100)
    monetization_fit: int = Field(..., ge=0, le=100)
    execution_difficulty: int = Field(..., ge=0, le=100)  # higher = harder
    risk: int = Field(..., ge=0, le=100)  # higher = riskier
    confidence: str = Field(..., description="Low/Medium/High")

class Competitor(BaseModel):
    name: str
    why_similar: str
    differentiation_tip: str

class ValidationResult(BaseModel):
    summary: str
    scores: ScoreBreakdown
    market_demand: Dict[str, Any]
    competitors: List[Competitor]
    risks: List[str]
    monetization: Dict[str, Any]
    mvp_roadmap: Dict[str, Any]
    next_actions: List[str]