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
    Classify a 333 message into INFORMATION, ASSISTANCE,
    EMERGENCY, or UNKNOWN.

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
        "fire",
        "critical",
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
        "solve",
        "support",
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


def _route_message(route: str) -> str:
    """
    Human-readable explanation of the route selected by SANG.
    """

    if route == "INFORMATION":
        return (
            "INFORMATION route activated. "
            "SANG will provide relevant information, resources, "
            "and available opportunities."
        )

    if route == "ASSISTANCE":
        return (
            "ASSISTANCE route activated. "
            "SANG will identify relevant people, resources, "
            "and opportunities that can help."
        )

    if route == "EMERGENCY":
        return (
            "EMERGENCY route activated. "
            "Prioritize immediate emergency-service or human escalation."
        )

    return (
        "The request could not be safely classified. "
        "Escalate to human assistance."
    )


def _routed_session(
    message: str,
    route: str,
    result=None,
) -> Dict:
    """
    Create a completed/routed 333 session.
    """

    return {
        "session_id": str(uuid4()),
        "channel": "333",
        "route": route,
        "original_message": message,
        "missing_information": [],
        "status": "ESCALATE" if route == "EMERGENCY" else "ROUTED",
        "action": _route_message(route),
        "prompt": None,
        "result": result,
    }


def start_333_session(message: str) -> Dict:
    """
    Start a simulated 333 interaction.
    """

    route = classify_333_intent(message)

    # ---------------------------------------------------------
    # EMERGENCY
    # ---------------------------------------------------------

    if route == "EMERGENCY":
        return _routed_session(
            message=message,
            route=route,
            result=None,
        )

    # ---------------------------------------------------------
    # UNKNOWN
    # ---------------------------------------------------------

    if route == "UNKNOWN":
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
            "prompt": (
                "I could not safely understand the request. "
                "Please try again or ask for human assistance."
            ),
            "result": None,
        }

    # ---------------------------------------------------------
    # INFORMATION
    # ---------------------------------------------------------

    if route == "INFORMATION":
        parsed = parse_agriculture_query(message)

        result = query_agriculture(message)

        return _routed_session(
            message=message,
            route=route,
            result=result,
        )

    # ---------------------------------------------------------
    # ASSISTANCE
    # ---------------------------------------------------------

    if route == "ASSISTANCE":
        parsed = parse_agriculture_query(message)

        if parsed["problem"] and not parsed["location_mentioned"]:
            session = _new_session(
                message=message,
                route=route,
                missing_information=["location"],
            )

            session["action"] = (
                "Ask the user for their location before routing "
                "the request to matching and assistance services."
            )

            session["prompt"] = (
                "I can help with that. What city or village are you in?"
            )

            return session

        result = query_agriculture(message)

        return _routed_session(
            message=message,
            route=route,
            result=result,
        )

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
            "action": (
                "This 333 session does not require additional information."
            ),
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