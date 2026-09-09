from typing import Dict


def build_voice_pipeline(
    transcript: str,
    route: str,
    response: Dict,
) -> Dict:
    """
    Builds an explainable representation of the
    Speak -> Think -> Speak pipeline.

    This is a prototype simulation of the 333
    voice interaction pipeline. Actual telephony
    deployment is outside the current prototype.
    """

    understood_text = transcript.strip()

    pipeline = [
        {
            "stage": "SPEAK",
            "status": "complete",
            "description": "Voice input received from the user.",
        },
        {
            "stage": "UNDERSTAND",
            "status": "complete",
            "description": "Speech was converted into text for SANG processing.",
            "transcript": understood_text,
        },
        {
            "stage": "CLASSIFY",
            "status": "complete",
            "description": f"SANG classified the request as {route}.",
            "route": route,
        },
        {
            "stage": "KNOWLEDGE",
            "status": "complete",
            "description": "SANG consulted the relevant prototype knowledge layer.",
        },
        {
            "stage": "MATCH",
            "status": "complete",
            "description": "SANG evaluated relevant people, resources, opportunities, or escalation paths.",
        },
        {
            "stage": "DECIDE",
            "status": "complete",
            "description": "SANG selected the appropriate response path.",
            "decision": route,
        },
        {
            "stage": "RESPOND",
            "status": "complete",
            "description": "SANG generated a response for the user.",
        },
        {
            "stage": "SPEAK",
            "status": "ready",
            "description": "The response can be spoken back to the user by the browser.",
            "response_text": response.get("message", ""),
        },
    ]

    return {
        "input_mode": "voice",
        "pipeline": pipeline,
    }