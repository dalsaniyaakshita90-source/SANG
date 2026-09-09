"""
SANG India-First Language Layer

Detects Indian-language user input and normalizes common
expressions into language-neutral SANG concepts.

Prototype languages:
- English
- Hindi
- Gujarati
- Marathi
- Bengali
- Tamil
- Telugu
- Kannada
- Malayalam
- Punjabi

Architecture:
User Language
      ↓
Language Detection
      ↓
Concept Normalization
      ↓
Language-Neutral SANG Query
      ↓
Existing SANG Intelligence
"""

from typing import Dict


SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "mr": "Marathi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
}


# ---------------------------------------------------------------------------
# SCRIPT DETECTION
# ---------------------------------------------------------------------------

SCRIPT_RANGES = {
    "gu": ("\u0A80", "\u0AFF"),
    "hi": ("\u0900", "\u097F"),
    "bn": ("\u0980", "\u09FF"),
    "pa": ("\u0A00", "\u0A7F"),
    "ta": ("\u0B80", "\u0BFF"),
    "te": ("\u0C00", "\u0C7F"),
    "kn": ("\u0C80", "\u0CFF"),
    "ml": ("\u0D00", "\u0D7F"),
    "mr": ("\u0900", "\u097F"),
}


def _contains_script(text: str, start: str, end: str) -> bool:
    return any(start <= char <= end for char in text)


# ---------------------------------------------------------------------------
# LANGUAGE DETECTION
# ---------------------------------------------------------------------------

ROMANIZED_MARKERS = {
    "hi": [
        "mujhe",
        "meri",
        "mera",
        "mere",
        "kisan",
        "kisan",
        "fasal",
        "paani",
        "pani",
        "sinchai",
        "mitti",
        "keede",
        "keeda",
        "keet",
        "madad",
        "chahiye",
        "samasya",
        "hai",
    ],
    "gu": [
        "mane",
        "mari",
        "maru",
        "mara",
        "khedut",
        "pak",
        "pani",
        "sinchai",
        "mati",
        "jivato",
        "madad",
        "joiye",
        "samasya",
        "chhe",
    ],
    "mr": [
        "mala",
        "majha",
        "maza",
        "shetkari",
        "pik",
        "pani",
        "mati",
        "kida",
        "madat",
        "havay",
        "samasya",
        "aahe",
    ],
    "bn": [
        "amar",
        "amake",
        "krishok",
        "foshol",
        "pani",
        "mati",
        "pokamakor",
        "sahajjo",
        "dorkar",
        "somossa",
    ],
    "ta": [
        "enakku",
        "en",
        "vivasayi",
        "payir",
        "thanneer",
        "mann",
        "poochi",
        "udhavi",
        "venum",
        "pirachanai",
    ],
    "te": [
        "naaku",
        "naa",
        "raitu",
        "panta",
        "neeru",
        "nela",
        "purugu",
        "sahayam",
        "kaavali",
        "samasya",
    ],
    "kn": [
        "nanage",
        "nanna",
        "raita",
        "bele",
        "neeru",
        "mannu",
        "keeta",
        "sahaya",
        "beku",
        "samasye",
    ],
    "ml": [
        "enikku",
        "ente",
        "karshakan",
        "vilavu",
        "vellam",
        "mannu",
        "keeda",
        "sahayam",
        "venam",
        "prashnam",
    ],
    "pa": [
        "mainu",
        "meri",
        "mera",
        "kisan",
        "fasal",
        "paani",
        "mitti",
        "keede",
        "madad",
        "chahidi",
        "samasiya",
    ],
}


def detect_language(text: str) -> str:
    """
    Detect the most likely supported Indian language.

    Priority:
    1. Gujarati script
    2. Bengali script
    3. Tamil script
    4. Telugu script
    5. Kannada script
    6. Malayalam script
    7. Punjabi / Gurmukhi script
    8. Devanagari
       - Marathi is detected through Marathi-specific Roman markers
       - otherwise Hindi
    9. Romanized language markers
    10. English fallback
    """

    if not text or not text.strip():
        return "en"

    text = text.strip()

    if _contains_script(text, *SCRIPT_RANGES["gu"]):
        return "gu"

    if _contains_script(text, *SCRIPT_RANGES["bn"]):
        return "bn"

    if _contains_script(text, *SCRIPT_RANGES["ta"]):
        return "ta"

    if _contains_script(text, *SCRIPT_RANGES["te"]):
        return "te"

    if _contains_script(text, *SCRIPT_RANGES["kn"]):
        return "kn"

    if _contains_script(text, *SCRIPT_RANGES["ml"]):
        return "ml"

    if _contains_script(text, *SCRIPT_RANGES["pa"]):
        return "pa"

    if _contains_script(text, *SCRIPT_RANGES["hi"]):
        lowered = text.lower()

        marathi_markers = [
            "मला",
            "माझा",
            "माझी",
            "शेतकरी",
            "पिक",
            "पाणी",
            "माती",
            "मदत",
            "समस्या",
            "आहे",
        ]

        if any(marker in text for marker in marathi_markers):
            return "mr"

        return "hi"

    lowered = text.lower()

    scores = {
        language: sum(
            1
            for marker in markers
            if marker in lowered
        )
        for language, markers in ROMANIZED_MARKERS.items()
    }

    best_language = max(
        scores,
        key=scores.get,
    )

    if scores[best_language] > 0:
        return best_language

    return "en"


# ---------------------------------------------------------------------------
# CONCEPT NORMALIZATION
# ---------------------------------------------------------------------------

NORMALIZATION_MAP = {
    # English
    "pests": "pest",
    "insect": "pest",
    "insects": "pest",
    "crop pest": "pest",
    "pest infestation": "pest",
    "pest": "pest",
    "crop insects": "pest",

    "watering": "irrigation",
    "water problem": "irrigation",
    "water shortage": "irrigation",
    "irrigation": "irrigation",

    "soil health": "soil",
    "soil": "soil",
    "soil issue": "soil",

    # Hindi / Hinglish
    "keeda lag gaya": "pest problem",
    "pest problem": "pest problem",
    "fasal mein keede": "pest problem",
    "fasal me keede": "pest problem",
    "keede": "pest problem",
    "keeda": "pest problem",
    "keet": "pest problem",

    "paani ki problem": "irrigation problem",
    "pani ki problem": "irrigation problem",
    "paani ki samasya": "irrigation problem",
    "pani ki samasya": "irrigation problem",
    "sinchai": "irrigation",

    "mitti ki problem": "soil problem",
    "mitti ki samasya": "soil problem",
    "mitti kharab": "soil problem",
    "mitti": "soil problem",

    # Gujarati / Roman Gujarati
    "jivato ni samasya": "pest problem",
    "pak ma jivato": "pest problem",
    "pakma jivato": "pest problem",
    "jivato": "pest",

    "pani ni samasya": "irrigation problem",
    "paani ni samasya": "irrigation problem",
    "sinchai ni samasya": "irrigation problem",

    "mati ni samasya": "soil problem",
    "mati": "soil",

    # Marathi / Roman Marathi
    "pikavar kide": "pest problem",
    "pikavar kida": "pest problem",
    "kida": "pest problem",
    "kide": "pest problem",

    "panyachi samasya": "irrigation problem",
    "pani chi samasya": "irrigationproblem",
    "sinchan": "irrigation",

    "matichi samasya": "soil problem",
    "mati kharab": "soil problem",

    # Bengali / Roman Bengali
    "pokamakor": "pest problem",
    "fosholer poka": "pest problem",
    "poka": "pest",

    "panir somossa": "irrigation problem",
    "joler somossa": "irrigation problem",

    "matir somossa": "soil",

    # Tamil / Roman Tamil
    "poochi": "pest",
    "poochi pirachanai": "pest problem",

    "thanneer pirachanai": "irrigation problem",
    "neer pirachanai": "irrigation problem",

    "mann pirachanai": "soil problem",

    # Telugu / Roman Telugu
    "purugu": "pest",
    "purugula samasya": "pest problem",

    "neeti samasya": "irrigation problem",
    "neeru samasya": "irrigation problem",

    "nela samasya": "soil problem",

    # Kannada / Roman Kannada
    "keeta": "pest",
    "keeta samasye": "pest problem",

    "neerina samasye": "irrigation problem",
    "neeru samasye": "irrigation problem",

    "mannina samasye": "soil problem",

    # Malayalam / Roman Malayalam
    "keeda": "pest",
    "keeda prashnam": "pest problem",

    "vellathinte prashnam": "irrigation problem",
    "vellam prashnam": "irrigation problem",

    "manninte prashnam": "soil problem",

    # Punjabi / Roman Punjabi
    "keede": "pest",
    "keeda": "pest",
    "fasal vich keede": "pest problem",

    "paani di samasiya": "irrigation problem",
    "pani di samasiya": "irrigation problem",

    "mitti di samasiya": "soil problem",
}


def normalize_query(text: str) -> str:
    """
    Convert common multilingual expressions into
    language-neutral SANG vocabulary.
    """

    normalized = text.lower().strip()

    replacements = sorted(
        NORMALIZATION_MAP.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for source, target in replacements:
        normalized = normalized.replace(
            source,
            target,
        )

    return normalized


# ---------------------------------------------------------------------------
# RESPONSE LANGUAGE
# ---------------------------------------------------------------------------

RESPONSE_TEMPLATES = {
    "en": {
        "location_prompt": (
            "I understand the agricultural problem. "
            "What city or village are you in?"
        ),
        "unknown": (
            "I couldn't understand the request clearly. "
            "Please describe the problem or information you need."
        ),
        "emergency": (
            "This is an emergency. Immediate human or "
            "emergency-service assistance should be prioritized."
        ),
    },

    "hi": {
        "location_prompt": (
            "मैं आपकी कृषि समस्या समझ गया। "
            "आप किस शहर या गाँव में हैं?"
        ),
        "unknown": (
            "मैं आपकी बात पूरी तरह समझ नहीं पाया। "
            "कृपया अपनी समस्या या आवश्यक जानकारी बताएं।"
        ),
        "emergency": (
            "यह एक आपातकालीन स्थिति है। "
            "तुरंत मानव या आपातकालीन सेवा की सहायता लें।"
        ),
    },

    "gu": {
        "location_prompt": (
            "હું તમારી ખેતીની સમસ્યા સમજી ગયો છું. "
            "તમે કયા શહેર અથવા ગામમાં છો?"
        ),
        "unknown": (
            "હું તમારી વિનંતીને સ્પષ્ટ રીતે સમજી શક્યો નથી. "
            "કૃપા કરીને તમારી સમસ્યા અથવા જરૂરી માહિતી જણાવો."
        ),
        "emergency": (
            "આ કટોકટીની સ્થિતિ છે. "
            "તરત જ માનવ અથવા કટોકટી સેવાની મદદ લો."
        ),
    },

    "mr": {
        "location_prompt": (
            "मला तुमची शेतीची समस्या समजली. "
            "तुम्ही कोणत्या शहरात किंवा गावात आहात?"
        ),
        "unknown": (
            "मला तुमची विनंती पूर्णपणे समजली नाही. "
            "कृपया तुमची समस्या किंवा आवश्यक माहिती सांगा."
        ),
        "emergency": (
            "ही आपत्कालीन परिस्थिती आहे. "
            "तात्काळ मानव किंवा आपत्कालीन सेवेची मदत घ्या."
        ),
    },

    "bn": {
        "location_prompt": (
            "আমি আপনার কৃষি সমস্যাটি বুঝতে পেরেছি। "
            "আপনি কোন শহর বা গ্রামে আছেন?"
        ),
        "unknown": (
            "আমি আপনার অনুরোধটি পরিষ্কারভাবে বুঝতে পারিনি। "
            "দয়া করে আপনার সমস্যা বা প্রয়োজনীয় তথ্য বলুন।"
        ),
        "emergency": (
            "এটি একটি জরুরি পরিস্থিতি। "
            "অবিলম্বে মানবিক বা জরুরি পরিষেবার সহায়তা নিন।"
        ),
    },

    "ta": {
        "location_prompt": (
            "உங்கள் விவசாயப் பிரச்சினையை நான் புரிந்துகொண்டேன். "
            "நீங்கள் எந்த நகரம் அல்லது கிராமத்தில் இருக்கிறீர்கள்?"
        ),
        "unknown": (
            "உங்கள் கோரிக்கையை தெளிவாக புரிந்துகொள்ள முடியவில்லை. "
            "தயவுசெய்து உங்கள் பிரச்சினையை அல்லது தேவையான தகவலை கூறுங்கள்."
        ),
        "emergency": (
            "இது அவசர நிலை. "
            "உடனடியாக மனிதர் அல்லது அவசர சேவையின் உதவியைப் பெறுங்கள்."
        ),
    },

    "te": {
        "location_prompt": (
            "మీ వ్యవసాయ సమస్య నాకు అర్థమైంది. "
            "మీరు ఏ నగరం లేదా గ్రామంలో ఉన్నారు?"
        ),
        "unknown": (
            "మీ అభ్యర్థనను నేను స్పష్టంగా అర్థం చేసుకోలేకపోయాను. "
            "దయచేసి మీ సమస్య లేదా అవసరమైన సమాచారాన్ని చెప్పండి."
        ),
        "emergency": (
            "ఇది అత్యవసర పరిస్థితి. "
            "వెంటనే మానవ సహాయం లేదా అత్యవసర సేవలను సంప్రదించండి."
        ),
    },

    "kn": {
        "location_prompt": (
            "ನಿಮ್ಮ ಕೃಷಿ ಸಮಸ್ಯೆ ನನಗೆ ಅರ್ಥವಾಗಿದೆ. "
            "ನೀವು ಯಾವ ನಗರ ಅಥವಾ ಗ್ರಾಮದಲ್ಲಿದ್ದೀರಿ?"
        ),
        "unknown": (
            "ನಿಮ್ಮ ವಿನಂತಿಯನ್ನು ನಾನು ಸ್ಪಷ್ಟವಾಗಿ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಿಲ್ಲ. "
            "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಸಮಸ್ಯೆ ಅಥವಾ ಅಗತ್ಯ ಮಾಹಿತಿಯನ್ನು ತಿಳಿಸಿ."
        ),
        "emergency": (
            "ಇದು ತುರ್ತು ಪರಿಸ್ಥಿತಿ. "
            "ತಕ್ಷಣ ಮಾನವ ಸಹಾಯ ಅಥವಾ ತುರ್ತು ಸೇವೆಯನ್ನು ಸಂಪರ್ಕಿಸಿ."
        ),
    },

    "ml": {
        "location_prompt": (
            "നിങ്ങളുടെ കാർഷിക പ്രശ്നം എനിക്ക് മനസ്സിലായി. "
            "നിങ്ങൾ ഏത് നഗരത്തിലോ ഗ്രാമത്തിലോ ആണ്?"
        ),
        "unknown": (
            "നിങ്ങളുടെ അഭ്യർത്ഥന എനിക്ക് വ്യക്തമായി മനസ്സിലായില്ല. "
            "ദയവായി നിങ്ങളുടെ പ്രശ്നമോ ആവശ്യമായ വിവരമോ പറയുക."
        ),
        "emergency": (
            "ഇത് അടിയന്തര സാഹചര്യമാണ്. "
            "ഉടൻ മനുഷ്യ സഹായമോ അടിയന്തര സേവനമോ തേടുക."
        ),
    },

    "pa": {
        "location_prompt": (
            "ਮੈਂ ਤੁਹਾਡੀ ਖੇਤੀਬਾੜੀ ਦੀ ਸਮੱਸਿਆ ਸਮਝ ਗਿਆ ਹਾਂ। "
            "ਤੁਸੀਂ ਕਿਹੜੇ ਸ਼ਹਿਰ ਜਾਂ ਪਿੰਡ ਵਿੱਚ ਹੋ?"
        ),
        "unknown": (
            "ਮੈਂ ਤੁਹਾਡੀ ਬੇਨਤੀ ਨੂੰ ਸਪਸ਼ਟ ਤੌਰ 'ਤੇ ਨਹੀਂ ਸਮਝ ਸਕਿਆ। "
            "ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਸਮੱਸਿਆ ਜਾਂ ਲੋੜੀਂਦੀ ਜਾਣਕਾਰੀ ਦੱਸੋ।"
        ),
        "emergency": (
            "ਇਹ ਐਮਰਜੈਂਸੀ ਸਥਿਤੀ ਹੈ। "
            "ਤੁਰੰਤ ਮਨੁੱਖੀ ਜਾਂ ਐਮਰਜੈਂਸੀ ਸੇਵਾ ਦੀ ਮਦਦ ਲਵੋ।"
        ),
    },
}


def translate_response(text: str, language: str) -> str:
    """
    Translate known SANG system responses.

    Arbitrary generated responses remain unchanged until
    a production translation provider is connected.
    """

    if language == "en":
        return text

    english_templates = RESPONSE_TEMPLATES["en"]
    target_templates = RESPONSE_TEMPLATES.get(
        language,
        {},
    )

    for key, english_text in english_templates.items():
        if text == english_text:
            return target_templates.get(
                key,
                text,
            )

    return text


# ---------------------------------------------------------------------------
# MAIN LANGUAGE PROCESSOR
# ---------------------------------------------------------------------------

def process_language(text: str) -> Dict:
    """
    Detect language and produce a normalized,
    language-neutral SANG representation.
    """

    language = detect_language(text)

    return {
        "original_text": text,
        "language": language,
        "language_name": SUPPORTED_LANGUAGES.get(
            language,
            "Unknown",
        ),
        "normalized_text": normalize_query(text),
        "supported": language in SUPPORTED_LANGUAGES,
    }


def get_response_language(language: str) -> str:
    """
    Return a supported response language.

    Unsupported languages safely fall back to English.
    """

    if language in SUPPORTED_LANGUAGES:
        return language

    return "en"