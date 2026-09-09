from backend.three_three_three import start_333_session


def test_hindi_agriculture_language_is_detected():
    session = start_333_session(
        "मेरी फसल में कीड़े लग गए हैं"
    )

    assert session["language"] == "hi"
    assert session["language_name"] == "Hindi"
    assert session["original_message"] == "मेरी फसल में कीड़े लग गए हैं"


def test_gujarati_agriculture_language_is_detected():
    session = start_333_session(
        "મારી ફસલમાં જીવાત લાગી છે"
    )

    assert session["language"] == "gu"
    assert session["language_name"] == "Gujarati"


def test_marathi_language_is_detected():
    session = start_333_session(
        "माझ्या पिकाला किडे लागले आहेत"
    )

    assert session["language"] == "mr"
    assert session["language_name"] == "Marathi"


def test_bengali_language_is_detected():
    session = start_333_session(
        "আমার ফসলে পোকা লেগেছে"
    )

    assert session["language"] == "bn"
    assert session["language_name"] == "Bengali"


def test_tamil_language_is_detected():
    session = start_333_session(
        "என் பயிரில் பூச்சி உள்ளது"
    )

    assert session["language"] == "ta"
    assert session["language_name"] == "Tamil"


def test_telugu_language_is_detected():
    session = start_333_session(
        "నా పంటలో పురుగులు ఉన్నాయి"
    )

    assert session["language"] == "te"
    assert session["language_name"] == "Telugu"


def test_kannada_language_is_detected():
    session = start_333_session(
        "ನನ್ನ ಬೆಳೆಯಲ್ಲಿ ಕೀಟಗಳಿವೆ"
    )

    assert session["language"] == "kn"
    assert session["language_name"] == "Kannada"


def test_malayalam_language_is_detected():
    session = start_333_session(
        "എന്റെ വിളയിൽ കീടങ്ങളുണ്ട്"
    )

    assert session["language"] == "ml"
    assert session["language_name"] == "Malayalam"


def test_punjabi_language_is_detected():
    session = start_333_session(
        "ਮੇਰੀ ਫਸਲ ਵਿੱਚ ਕੀੜੇ ਹਨ"
    )

    assert session["language"] == "pa"
    assert session["language_name"] == "Punjabi"


def test_english_language_is_detected():
    session = start_333_session(
        "I have a pest problem in Rajkot"
    )

    assert session["language"] == "en"
    assert session["language_name"] == "English"

def test_hindi_pest_normalizes_to_sang_concept():
    session = start_333_session(
        "Meri fasal mein keede lag gaye hain"
    )

    assert session["language"] == "hi"
    assert "pest" in session["normalized_message"]


def test_gujarati_irrigation_normalizes_to_sang_concept():
    session = start_333_session(
        "Mane pani ni samasya chhe"
    )

    assert session["language"] == "gu"
    assert "irrigation" in session["normalized_message"]


def test_hindi_soil_normalizes_to_sang_concept():
    session = start_333_session(
        "Mitti ki problem hai"
    )

    assert session["language"] == "hi"
    assert "soil" in session["normalized_message"]


def test_marathi_pest_normalizes_to_sang_concept():
    session = start_333_session(
        "Mala pikavar kide ahet"
    )

    assert session["language"] == "mr"
    assert "pest" in session["normalized_message"]

def test_hindi_pest_routes_to_assistance():
    session = start_333_session(
        "Meri fasal mein keede lag gaye hain Rajkot mein"
    )

    assert session["language"] == "hi"
    assert session["route"] == "ASSISTANCE"
    assert session["result"]["understood"]["problem"] == "Crop Pest Infestation"
    assert session["result"]["results"]


def test_gujarati_irrigation_routes_to_assistance():
    session = start_333_session(
        "Mane Ahmedabad ma pani ni samasya chhe"
    )

    assert session["language"] == "gu"
    assert session["route"] == "ASSISTANCE"
    assert session["result"]["understood"]["problem"] == "Irrigation Challenge"
    assert session["result"]["results"]


def test_hindi_soil_routes_to_assistance():
    session = start_333_session(
        "Mitti ki problem hai Surat mein"
    )

    assert session["language"] == "hi"
    assert session["route"] == "ASSISTANCE"
    assert session["result"]["understood"]["problem"] == "Soil Health Problem"
    assert session["result"]["results"]


def test_marathi_pest_routes_to_assistance():
    session = start_333_session(
        "Mala Rajkot madhe pikavar kide ahet"
    )

    assert session["language"] == "mr"
    assert session["route"] == "ASSISTANCE"
    assert session["result"]["understood"]["problem"] == "Crop Pest Infestation"
    assert session["result"]["results"]

