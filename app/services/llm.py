import json
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

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

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
def generate_analysis_with_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        return { ... }

    user_prompt = f"""
    INPUT:
    idea: {payload.get("idea")}
    target_users: {payload.get("target_users")}
    business_type: {payload.get("business_type")}
    region: {payload.get("region")}
    category: {payload.get("category")}
    unique_edge: {payload.get("unique_edge")}
    """.strip()

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},  # ✅ supported here
        temperature=0.4,
    )

    content = resp.choices[0].message.content or "{}"
    return json.loads(content)