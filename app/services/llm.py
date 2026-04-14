import json
import logging
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI
from app.core.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

SYSTEM_PROMPT = """
You are LaunchLens, a product idea validator.

Return ONLY valid JSON with this exact shape (no markdown, no extra keys):

Rules:
- Return ONLY valid JSON. No markdown. No extra keys.
- Scores must be integers 0-100.
- Competitors: prefer real, widely-known products in the same category. If unsure, use realistic category-based competitors (e.g. "Notion templates", "Google Sheets workflows", "Generic competitor: <category tool>") rather than "ExampleCompetitor".
- Summary must be 5–8 sentences and include:
  1) who the ideal customer is (ICP),
  2) the core pain point + why now,
  3) the sharpest differentiation angle,
  4) the biggest risk,
  5) a tight MVP recommendation (what to build first),
  6) a simple go-to-market suggestion.

- Risks: 4–6 bullets, specific and practical (not generic).
- Next actions: 5–7 bullets, ordered by what to do first this week.

{
  "demand": 0-100,
  "competition": 0-100,
  "differentiation": 0-100,
  "monetization_fit": 0-100,
  "execution_difficulty": 0-100,
  "risk": 0-100,
  "confidence": "Low"|"Medium"|"High",
  "summary": "string",
  "market_demand": { "signals": ["..."], "positioning": ["..."] },
  "competitors": [{ "name":"...", "why_similar":"...", "differentiation_tip":"..." }],
  "risks": ["..."],
  "monetization": { "models":["..."], "suggested_pricing":["..."] },
  "mvp_roadmap": { "2_weeks":["..."], "30_days":["..."], "90_days":["..."] },
  "next_actions": ["..."]
}
""".strip()


def _mock_response() -> Dict[str, Any]:
    """Fallback response when no API key is configured."""
    return {
        "demand": 60,
        "competition": 50,
        "differentiation": 55,
        "monetization_fit": 60,
        "execution_difficulty": 50,
        "risk": 45,
        "confidence": "Medium",
        "summary": (
            "This is a mock analysis generated because no OpenAI API key is configured. "
            "The target users appear to have a real pain point worth exploring. "
            "Differentiation will be key in this space. "
            "The biggest risk is market timing and customer acquisition cost. "
            "Start with a simple landing page MVP to validate demand before building. "
            "Focus on a single customer segment first before expanding."
        ),
        "market_demand": {
            "signals": ["Growing interest in this category", "Existing tools have known gaps"],
            "positioning": ["Focus on ease of use", "Target underserved niche first"],
        },
        "competitors": [
            {
                "name": "Existing Category Leader",
                "why_similar": "Solves the same core problem",
                "differentiation_tip": "Go narrower and faster for a specific use case",
            }
        ],
        "risks": [
            "Customer acquisition cost may be high",
            "Larger competitors could copy the feature",
            "Market may not be ready for this solution yet",
            "Execution complexity could delay launch",
        ],
        "monetization": {
            "models": ["Freemium", "Monthly subscription"],
            "suggested_pricing": ["Free tier to drive adoption", "$29/month for pro features"],
        },
        "mvp_roadmap": {
            "2_weeks": ["Build landing page", "Validate with 10 potential users"],
            "30_days": ["Ship core feature", "Get 5 paying customers"],
            "90_days": ["Iterate based on feedback", "Reach $1k MRR"],
        },
        "next_actions": [
            "Interview 5 potential customers this week",
            "Build a landing page to test messaging",
            "Define your one core differentiator",
            "Identify your lowest-cost acquisition channel",
            "Set a clear 30-day launch goal",
        ],
    }


@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
def generate_analysis_with_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not OPENAI_API_KEY or client is None:
        logger.warning("OPENAI_API_KEY not set — returning mock response")
        return _mock_response()

    user_prompt = f"""
    INPUT:
    idea: {payload.get("idea")}
    target_users: {payload.get("target_users")}
    business_type: {payload.get("business_type")}
    region: {payload.get("region")}
    category: {payload.get("category")}
    unique_edge: {payload.get("unique_edge")}
    """.strip()

    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
        )
        content = resp.choices[0].message.content or "{}"
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        return _mock_response()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON: {e}")
        return _mock_response()
