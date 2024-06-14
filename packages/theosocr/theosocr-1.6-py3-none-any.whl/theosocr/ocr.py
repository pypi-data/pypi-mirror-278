import requests

def theos_ocr_file(filename, overlay=False, language='eng'):
    """
    
    :param filename: Resim dosyasının adı.
    :param overlay: Overlay özelliği.
    :param language: Dili belirleyin (varsayılan: 'eng').
    :return: JSON yanıtı.
    """
    api_key = 'K82904583288957'
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    result=r.json()
    parsed_text = result['ParsedResults'][0]['ParsedText'].strip().replace('\r\n', '')
    return parsed_text
  
