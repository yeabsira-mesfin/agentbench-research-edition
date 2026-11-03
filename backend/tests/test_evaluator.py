from app.evaluator import evaluate

def test_weighted_score():
    result = evaluate({"correctness":100,"security":80,"tests":80,"maintainability":60,"documentation":70})
    assert result["score"] == 84.0
    assert result["grade"] == "strong"

def test_scores_are_clamped():
    result = evaluate({"correctness":120,"security":-20,"tests":100,"maintainability":100,"documentation":100})
    assert result["dimensions"]["correctness"] == 100
    assert result["dimensions"]["security"] == 0

