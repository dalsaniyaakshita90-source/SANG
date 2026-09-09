from typing import Optional


KNOWLEDGE_BASE = {
    "crop insurance": {
        "answer": (
            "Crop insurance is a type of insurance that protects farmers "
            "against financial losses caused by events such as crop failure, "
            "natural disasters, pests, diseases, and other covered risks. "
            "Farmers pay a premium, and eligible losses can be compensated "
            "according to the terms of the insurance policy."
        ),
        "topic": "Agriculture",
    },

    "soil health": {
        "answer": (
            "Soil health describes how well soil functions as a living system "
            "that supports plant growth. Healthy soil generally has good "
            "structure, nutrients, water-holding capacity, and biological "
            "activity."
        ),
        "topic": "Agriculture",
    },

    "drip irrigation": {
        "answer": (
            "Drip irrigation delivers water directly to the root zone of "
            "plants through small emitters. It can reduce water loss from "
            "evaporation and runoff and can help farmers use irrigation water "
            "more efficiently."
        ),
        "topic": "Agriculture",
    },

    "crop pest": {
        "answer": (
            "Crop pests are insects or other organisms that can damage crops "
            "and reduce yields. Pest management can involve monitoring crops, "
            "identifying the pest correctly, and using appropriate cultural, "
            "biological, mechanical, or chemical control methods."
        ),
        "topic": "Agriculture",
    },

    "irrigation": {
        "answer": (
            "Irrigation is the artificial application of water to crops when "
            "rainfall is not sufficient. Different systems, including drip "
            "and sprinkler irrigation, can help manage water according to "
            "crop and soil needs."
        ),
        "topic": "Agriculture",
    },
}


def answer_information(query: str) -> Optional[dict]:
    """
    Find a relevant knowledge-base answer for an information request.
    Returns None when no reliable answer is available.
    """

    text = query.lower().strip()

    # Check the most specific phrases first.
    keywords = sorted(
        KNOWLEDGE_BASE.keys(),
        key=len,
        reverse=True,
    )

    for keyword in keywords:
        if keyword in text:
            entry = KNOWLEDGE_BASE[keyword]

            return {
                "query": query,
                "answered": True,
                "topic": entry["topic"],
                "answer": entry["answer"],
                "source": "SANG agriculture knowledge base",
            }

    return {
        "query": query,
        "answered": False,
        "answer": (
            "I understand that you are asking for information, "
            "but I do not currently have a verified answer for that question. "
            "I can connect you with a human or relevant SANG resource."
        ),
        "source": "SANG knowledge layer",
    }
