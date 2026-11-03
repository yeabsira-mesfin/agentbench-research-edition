from dataclasses import dataclass

WEIGHTS = {"correctness": 0.40, "security": 0.20, "tests": 0.15, "maintainability": 0.15, "documentation": 0.10}

@dataclass(frozen=True)
class Evaluation:
    correctness: float
    security: float
    tests: float
    maintainability: float
    documentation: float

    def total(self) -> float:
        values = self.__dict__
        return round(sum(values[k] * WEIGHTS[k] for k in WEIGHTS), 2)

    def grade(self) -> str:
        score = self.total()
        if score >= 90: return "excellent"
        if score >= 80: return "strong"
        if score >= 70: return "acceptable"
        return "needs_improvement"

def evaluate(payload: dict) -> dict:
    clean = {}
    for key in WEIGHTS:
        value = float(payload.get(key, 0))
        clean[key] = max(0.0, min(100.0, value))
    result = Evaluation(**clean)
    return {"score": result.total(), "grade": result.grade(), "weights": WEIGHTS, "dimensions": clean}

