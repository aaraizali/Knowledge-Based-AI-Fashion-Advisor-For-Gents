# advisor.py
import json
from typing import List, Dict, Any, Tuple, Optional

RULES_FILE = "rules.json"

def load_rules() -> List[Dict[str, Any]]:
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("rules", [])

def save_rules(rules: List[Dict[str, Any]]) -> None:
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump({"rules": rules}, f, indent=4, ensure_ascii=False)

def normalize(text: str) -> str:
    return text.strip().lower() if isinstance(text, str) else ""

def score_rule(
    rule: Dict[str, Any],
    weather: str,
    occasion: str,
    body_type: str,
    style: str,
    preferred_colors: List[str]
) -> tuple[int, List[str], List[str]]:
    score = 0
    fired: List[str] = []
    reasons: List[str] = []

    if normalize(rule.get("weather", "")) == normalize(weather):
        score += 4
        fired.append("R_weather")
        reasons.append(f"Rule {rule.get('id')}: weather matches ({weather}).")

    if normalize(rule.get("occasion", "")) == normalize(occasion):
        score += 4
        fired.append("R_occasion")
        reasons.append(f"Rule {rule.get('id')}: occasion matches ({occasion}).")

    if normalize(rule.get("body_type", "")) == normalize(body_type):
        score += 3
        fired.append("R_body_type")
        reasons.append(f"Rule {rule.get('id')}: body type matches ({body_type}).")

    if normalize(rule.get("style", "")) == normalize(style):
        score += 2
        fired.append("R_style")
        reasons.append(f"Rule {rule.get('id')}: style preference matches ({style}).")

    if preferred_colors:
        rule_colors = [normalize(c) for c in rule.get("colors", [])]
        matched: List[str] = []
        for c in preferred_colors:
            if normalize(c) in rule_colors:
                matched.append(c)
        if matched:
            score += 2 * len(matched)
            fired.append("R_color")
            reasons.append(f"Rule {rule.get('id')}: preferred colors matched ({', '.join(matched)}).")

    bottom = normalize(rule.get("bottom", ""))
    if "short" in bottom and normalize(occasion) == "formal":
        score -= 5
        fired.append("R_penalty_shorts_formal")
        reasons.append(f"Rule {rule.get('id')}: shorts are not suitable for formal occasion.")

    return score, fired, reasons

def get_recommendation(
    weather: str,
    occasion: str,
    body_type: str,
    style: Optional[str] = None,
    preferred_colors: Optional[List[str]] = None,
    top_n: int = 3
) -> List[Dict[str, Any]]:
    rules = load_rules()
    scored: List[Dict[str, Any]] = []

    for rule in rules:
        sc, fired, reasons = score_rule(rule, weather, occasion, body_type, style or "", preferred_colors or [])
        scored.append({
            "rule": rule,
            "score": sc,
            "fired": fired,
            "reasons": reasons
        })

    scored_sorted = sorted(scored, key=lambda x: (-x["score"], x["rule"].get("id", 0)))

    results: List[Dict[str, Any]] = []
    for entry in scored_sorted:
        if len(results) >= top_n:
            break
        results.append({
            "top": entry["rule"].get("top"),
            "bottom": entry["rule"].get("bottom"),
            "shoes": entry["rule"].get("shoes"),
            "accessories": entry["rule"].get("accessories"),
            "colors": entry["rule"].get("colors"),
            "rule_id": entry["rule"].get("id"),
            "score": entry["score"],           # lowercase
            "applied_rules": entry["fired"],  # lowercase
            "reasoning": entry["reasons"]     # lowercase
        })

    return results
