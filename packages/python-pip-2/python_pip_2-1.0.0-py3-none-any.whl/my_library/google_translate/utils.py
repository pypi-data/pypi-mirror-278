def format_translation_response(response):
    try:
        translated_text = response['data']['translations'][0]['translatedText']
        return translated_text
    except (KeyError, IndexError) as e:
        raise ValueError("Invalid response format") from e
