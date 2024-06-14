
import requests

def theos_ocr_base64(base64_image, overlay=False, language='eng', api_key='K82904583288957'):
    """
    OCR.space API kullanarak base64 kodlu resim verisinden metin çıkarır.
    :param base64_image: Base64 kodlu resim verisi.
    :param overlay: Overlay özelliği.
    :param language: Dili belirleyin (varsayılan: 'eng').
    :param api_key: API anahtarınız.
    :return: JSON yanıtı.
    """
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
        'base64Image': base64_image,
    }
    r = requests.post('https://api.ocr.space/parse/image', data=payload)
    result=r.json()
    parsed_text = result['ParsedResults'][0]['ParsedText'].strip().replace('\r\n', '')
    return parsed_text
  
