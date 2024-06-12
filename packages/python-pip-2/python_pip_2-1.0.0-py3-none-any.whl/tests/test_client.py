import pytest
from unittest.mock import Mock, patch
from my_library.google_translate.client import GoogleTranslateClient
from my_library.google_translate.utils import format_translation_response
from my_library.data_processing.clean import clean_text
from my_library.data_processing.transform import transform_text

def test_clean_text():
    text = "  Hello, World!  "
    cleaned_text = clean_text(text)
    assert cleaned_text == "hello, world!"

def test_transform_text():
    text = "Hello, World!"
    transformed_text = transform_text(text)
    assert transformed_text == "HELLO, WORLD!"

def test_format_translation_response():
    response = {
        "data": {
            "translations": [
                {"translatedText": "Hola, Mundo!"}
            ]
        }
    }
    formatted_text = format_translation_response(response)
    assert formatted_text == "Hola, Mundo!"

@patch('my_library.google_translate.client.requests.post')
def test_translate_text(mock_post):
    # Mocking the API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "translations": [
                {"translatedText": "Hola, Mundo!"}
            ]
        }
    }
    mock_post.return_value = mock_response

    api_key = 'fake_api_key'
    client = GoogleTranslateClient(api_key)
    response = client.translate_text("Hello, World!", "es")
    translated_text = format_translation_response(response)
    
    assert translated_text == "Hola, Mundo!"

if __name__ == "__main__":
    pytest.main()
