from typing import Dict


COUNTRY_RULESETS = {
    "IN": {
        "country": "India",
        "emergency_services": {
            "medical": {
                "service": "Medical Emergency Service",
                "number": "108",
                "action": (
                    "Call 108 immediately for ambulance and medical emergency assistance."
                ),
            },
            "fire": {
                "service": "Fire & Rescue Service",
                "number": "101",
                "action": (
                    "Call 101 immediately for fire and rescue assistance."
                ),
            },
            "police": {
                "service": "Police Emergency Service",
                "number": "112",
                "action": (
                    "Call 112 immediately for police and emergency assistance."
                ),
            },
            "general": {
                "service": "Emergency Response Service",
                "number": "112",
                "action": (
                    "Call 112 immediately for emergency assistance."
                ),
            },
        },
    },
}


DEFAULT_COUNTRY = "IN"


def get_country_ruleset(country_code: str = DEFAULT_COUNTRY) -> Dict:
    """
    Return the emergency ruleset for a country.

    SANG v1 is India-first. Future countries can be added
    without changing the emergency classification logic.
    """
    return COUNTRY_RULESETS.get(
        country_code.upper(),
        COUNTRY_RULESETS[DEFAULT_COUNTRY],
    )


def classify_emergency_type(message: str) -> str:
    text = message.lower().strip()

    medical_keywords = [
        "medical",
        "ambulance",
        "heart attack",
        "stroke",
        "bleeding",
        "unconscious",
        "injury",
        "injured",
        "accident",
        "breathing",
        "breathless",
        "poison",
        "poisoning",
        "fainted",
        "fainting",
    ]

    fire_keywords = [
        "fire",
        "burning",
        "smoke",
        "flames",
    ]

    police_keywords = [
        "police",
        "robbery",
        "theft",
        "crime",
        "attack",
        "violence",
        "threat",
        "danger",
    ]

    if any(keyword in text for keyword in medical_keywords):
        return "medical"

    if any(keyword in text for keyword in fire_keywords):
        return "fire"

    if any(keyword in text for keyword in police_keywords):
        return "police"

    return "general"


def identify_emergency(
    message: str,
    country_code: str = DEFAULT_COUNTRY,
) -> Dict:
    """
    Identify the emergency type and route it through the
    appropriate country-specific emergency ruleset.
    """

    emergency_type = classify_emergency_type(message)

    ruleset = get_country_ruleset(country_code)
    services = ruleset["emergency_services"]
    service = services[emergency_type]

    return {
        "detected": True,
        "country": ruleset["country"],
        "country_code": country_code.upper(),
        "emergency_type": emergency_type,
        "service": service["service"],
        "contact": service["number"],
        "action": service["action"],
        "escalation": "IMMEDIATE",
        "source": "SANG emergency routing layer",
    }