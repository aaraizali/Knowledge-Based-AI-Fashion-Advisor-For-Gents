# advisor.py
from rules import rules
import random

def get_recommendation(weather, occasion, body_type, style=None, preferred_colors=None):
    outfits = []

    for i in range(3):  # Generate 3 outfit options
        outfit = {}
        reasoning = []

        # Weather-based selection
        weather_rule = rules["weather"].get(weather)
        if weather_rule:
            outfit["Top"] = random.choice(weather_rule["top"])
            outfit["Bottom"] = random.choice(weather_rule["bottom"])
            outfit["Shoes"] = random.choice(weather_rule["shoes"])
            reasoning.append(weather_rule["reason"])

        # Occasion-based selection
        occasion_rule = rules["occasion"].get(occasion)
        if occasion_rule:
            outfit["Occasion Add-on"] = random.choice(occasion_rule["addon"])
            outfit["Occasion Shoes"] = random.choice(occasion_rule["shoes"])
            reasoning.append(occasion_rule["reason"])

        # Body type advice
        body_rule = rules["body_type"].get(body_type)
        if body_rule:
            outfit["Fit Advice"] = body_rule["fit"]
            reasoning.append(body_rule["fit"])

        # Style advice
        if style:
            style_rule = rules["style"].get(style)
            if style_rule:
                reasoning.append(style_rule["pattern"])

        # Preferred colors
        if preferred_colors:
            reasoning.append(f"Preferred colors considered: {', '.join(preferred_colors)}")

        outfit["reasoning"] = reasoning
        outfits.append(outfit)

    return outfits
