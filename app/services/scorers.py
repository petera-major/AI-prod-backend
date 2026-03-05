def clamp(n: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, n))

def compute_viability_score(
    demand: int,
    competition: int,
    differentiation: int,
    monetization_fit: int,
    execution_difficulty: int,
    risk: int
) -> int:
    score = (
        0.30 * demand +
        0.20 * (100 - competition) +
        0.15 * differentiation +
        0.10 * monetization_fit +
        0.15 * (100 - execution_difficulty) +
        0.10 * (100 - risk)
    )
    return clamp(int(round(score)))