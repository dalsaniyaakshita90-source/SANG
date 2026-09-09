from backend.language_layer import (
    detect_language,
    normalize_query,
    process_language,
    get_response_language,
)


def test_detect_english():
    assert detect_language("I have a pest problem in Rajkot") == "en"


def test_detect_hindi_script():
    assert detect_language("मेरी फसल में कीड़े लग गए हैं") == "hi"


def test_detect_gujarati_script():
    assert detect_language("મારી ફસલમાં જીવાત લાગી છે") == "gu"


def test_detect_hinglish():
    assert detect_language(
        "Meri fasal mein keede lag gaye hain"
    ) == "hi"


def test_detect_gujarati_romanized():
    assert detect_language(
        "Mane pani ni samasya chhe"
    ) == "gu"


def test_normalize_pest():
    result = normalize_query(
        "Meri fasal mein keede lag gaye hain"
    )

    assert "pest" in result


def test_normalize_irrigation():
    result = normalize_query(
        "Mane pani ni samasya chhe"
    )

    assert "irrigation" in result


def test_normalize_soil():
    result = normalize_query(
        "Mitti ki problem hai"
    )

    assert "soil" in result


def test_process_language():
    result = process_language(
        "मेरी फसल में कीड़े लग गए हैं"
    )

    assert result["language"] == "hi"
    assert result["language_name"] == "Hindi"
    assert result["supported"] is True
    assert result["original_text"]


def test_supported_response_language():
    assert get_response_language("hi") == "hi"
    assert get_response_language("gu") == "gu"
    assert get_response_language("en") == "en"


def test_unsupported_response_language_falls_back():
    assert get_response_language("xx") == "en"