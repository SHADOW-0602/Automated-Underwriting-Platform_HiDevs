import json
import os

# Load configuration from config.json
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    POTENTIAL_RISK_OBJECTS = config['potential_risk_objects']
    COMPLIANCE_CHECKLIST = config['compliance_checklist']
except FileNotFoundError:
    raise FileNotFoundError("config.json not found. Please ensure it exists in the project directory.")
except json.JSONDecodeError:
    raise ValueError("Invalid config.json format. Please check the JSON syntax.")

def evaluate_risk(doc_analysis, image_analysis):
    """
    Evaluates property risk based on document and image analysis using a rule-based system.
    Combines fusion, scoring, and compliance logic. Risk rules and compliance checks are
    defined in config.json for easy modification.

    Args:
        doc_analysis (dict): Output from document_processor.analyze_document_text.
        image_analysis (dict): Output from image_analyzer.analyze_property_images.

    Returns:
        A dictionary containing the risk score, reasoning, and compliance check.

    Raises:
        ValueError: If input dictionaries are invalid or missing required keys.
    """
    # Input validation
    if not isinstance(doc_analysis, dict) or not isinstance(image_analysis, dict):
        raise ValueError("doc_analysis and image_analysis must be dictionaries.")
    if 'risk_keywords' not in doc_analysis or 'risk_tags' not in image_analysis:
        raise ValueError("Required keys missing in input dictionaries.")

    score = 0
    reasoning = []
    compliance_issues = []

    # --- Risk Scoring Logic ---
    # Rule 1: High-risk keywords in the document significantly increase the score.
    high_risk_doc_keywords = ['fire', 'asbestos', 'structural_damage']
    for keyword in doc_analysis['risk_keywords']:
        if keyword in high_risk_doc_keywords:
            score += 40
            reasoning.append(f"High-risk keyword '{keyword}' found in document.")
        else:
            score += 15
            reasoning.append(f"Potential risk keyword '{keyword}' found in document.")

    # Rule 2: Risk-tagged objects from images increase the score.
    if image_analysis['risk_tags']:
        score += 20 * len(image_analysis['risk_tags'])
        reasoning.append(f"Detected potential risk objects in images: {', '.join(image_analysis['risk_tags'])}")

    # Rule 3 (Hybrid): Combine document and image insights.
    if 'leak' in doc_analysis['risk_keywords'] and 'potted plant' in image_analysis['risk_tags']:
        score += 25
        reasoning.append("Combined Risk: Document mentions 'leak' and images show potential moisture sources.")

    # --- Final Score Classification ---
    if score > 70:
        risk_level = "High"
    elif score > 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    if not reasoning:
        reasoning.append("No specific risk indicators found. Standard assessment.")

    # --- Compliance Checker ---
    for keyword, issue in COMPLIANCE_CHECKLIST.items():
        if keyword in doc_analysis['risk_keywords']:
            compliance_issues.append(issue)

    if not compliance_issues:
        compliance_issues.append("No major compliance issues flagged based on keyword search.")

    return {
        "risk_score": min(score, 100),  # Cap score at 100
        "risk_level": risk_level,
        "reasoning": reasoning,
        "compliance_report": compliance_issues
    }