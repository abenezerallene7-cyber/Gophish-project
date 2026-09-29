SEVERITY_WEIGHTS = {
    'Critical': 40,
    'High': 20,
    'Medium': 10,
    'Low': 5,
    'Info': 0
}

CATEGORY_MULTIPLIERS = {
    'SSL': 1.2,
    'Headers': 1.0,
    'DNS': 1.1,
    'Reputation': 1.5,
    'Email': 1.0,
    'Network': 1.3,
    'Vulnerability': 1.8,
    'Technology': 0.5,
    'General': 1.0
}

def calculate_risk_score(findings):
    total = 0
    for f in findings:
        severity = f.get('severity', 'Info')
        weight = SEVERITY_WEIGHTS.get(severity, 0)
        category = f.get('category', 'General')
        multiplier = CATEGORY_MULTIPLIERS.get(category, 1.0)
        total += weight * multiplier
    score = min(100, int(total))
    if score <= 25:
        level = 'Low'
    elif score <= 50:
        level = 'Medium'
    elif score <= 75:
        level = 'High'
    else:
        level = 'Critical'
    return score, level