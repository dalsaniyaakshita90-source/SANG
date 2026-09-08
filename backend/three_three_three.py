from typing import Dict, Optional
from uuid import uuid4

from backend.agriculture_query import (
    parse_agriculture_query,
    query_agriculture,
)


ROUTES = {
    "information": "INFORMATION",
    "assistance": "ASSISTANCE",
    "emergency": "EMERGENCY",
}


def classify_333_intent(message: str) -> str:
    """
    Classify a 333 user message into one of the three core routes.

    This is a deterministic prototype classifier.
    """

    text = message.lower().strip()

    emergency_keywords = [
        "emergency",
        "urgent",
        "help now",
        "accident",
        "danger",
        "bleeding",
        "unconscious",
    ]

    assistance_keywords = [
        "help me",
        "can you help",
        "need help",
        "find someone",
        "connect me",
        "get medicine",
        "get a medicine",
        "apply",
        "access",
    ]

    information_keywords = [
        "what is",
        "where is",
        "how do",
        "information",
        "scheme",
        "market",
        "price",
        "weather",
        "hospital",
        "agriculture",
        "farmer",
        "crop",
        "pest",
        "irrigation",
        "soil",
    ]

    if any(keyword in text for keyword in emergency_keywords):
        return ROUTES["emergency"]

    if any(keyword in text for keyword in assistance_keywords):
        return ROUTES["assistance"]

    if any(keyword in text for keyword in information_keywords):
        return ROUTES["information"]

    return "UNKNOWN"


def _new_session(
    message: str,
    route: str,
    missing_information: Optional[list] = None,
) -> Dict:
    """
    Create a lightweight in-memory 333 session.
    """

    return {
        "session_id": str(uuid4()),
        "channel": "333",
        "route": route,
        "original_message": message,
        "missing_information": missing_information or [],
        "status": "NEEDS_INFORMATION",
    }


def start_333_session(message: str) -> Dict:
    """
    Start a new simulated 333 interaction.
    """

    route = classify_333_intent(message)

    if route in {"INFORMATION", "ASSISTANCE"}:
        parsed = parse_agriculture_query(message)

        if parsed["problem"] and not parsed["location_mentioned"]:
            session = _new_session(
                message=message,
                route=route,
                missing_information=["location"],
            )

            session["action"] = (
                "Ask the user for their location before routing the request."
            )
            session["prompt"] = (
                "I can help with that. What city or village are you in?"
            )

            return session

        return {
            "session_id": str(uuid4()),
            "channel": "333",
            "route": route,
            "original_message": message,
            "missing_information": [],
            "status": "ROUTED",
            "action": (
                "Route the request to SANG information and knowledge services."
                if route == "INFORMATION"
                else "Route the request to SANG matching and assistance services."
            ),
            "prompt": None,
            "result": query_agriculture(message),
        }

    if route == "EMERGENCY":
        return {
            "session_id": str(uuid4()),
            "channel": "333",
            "route": route,
            "original_message": message,
            "missing_information": [],
            "status": "ESCALATE",
            "action": (
                "Prioritize immediate emergency-service or human escalation. "
                "Do not depend on a long AI conversation."
            ),
            "prompt": None,
            "result": None,
        }

    return {
        "session_id": str(uuid4()),
        "channel": "333",
        "route": "UNKNOWN",
        "original_message": message,
        "missing_information": [],
        "status": "ESCALATE",
        "action": (
            "The request could not be safely classified. "
            "Escalate to human assistance."
        ),
        "prompt": None,
        "result": None,
    }


def continue_333_session(session: Dict, message: str) -> Dict:
    """
    Continue an existing 333 session using the user's follow-up message.
    """

    if session["status"] != "NEEDS_INFORMATION":
        return {
            **session,
            "follow_up_message": message,
            "status": "COMPLETED",
            "action": "This 333 session does not require additional information.",
        }

    combined_message = (
        f"{session['original_message']} {message}"
    )

    result = query_agriculture(combined_message)

    if result["results"]:
        return {
            **session,
            "follow_up_message": message,
            "status": "ROUTED",
            "missing_information": [],
            "action": (
                "The missing information was received. "
                "Route the request to SANG matching and assistance services."
            ),
            "prompt": None,
            "result": result,
        }

    return {
        **session,
        "follow_up_message": message,
        "status": "NEEDS_INFORMATION",
        "action": (
            "The additional information was not sufficient to safely "
            "resolve the request. Ask for clarification or escalate."
        ),
        "prompt": (
            "I still need a little more information to help you safely."
        ),
        "result": None,
    }


def route_333(message: str) -> Dict:
    """
    Backward-compatible single-message 333 routing function.
    """

    return start_333_session(message)