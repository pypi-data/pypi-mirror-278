# TheosOCR

This is a simple OCR library that uses the Theos OCR API to extract text from images.

## Installation

```bash
pip install theosocr
```
## use 
```python
from theosocr import theos_ocr_file, theos_ocr_base64

# OCR işlemi yapılacak dosya adı
file_path = 'path_to_your_image.png'

# Dosya yoluyla OCR işlemi
result_file = theos_ocr_file(file_path)

# Base64 stringi oluşturma
def image_to_base64(file_path):
    with open(file_path, 'rb') as image_file:
        base64_bytes = base64.b64encode(image_file.read())
        base64_string = base64_bytes.decode('utf-8')
    return base64_string

base64_image = image_to_base64(file_path)

# Base64 ile OCR işlemi
result_base64 = theos_ocr_base64(base64_image)

# Sonuçları yazdırın
print("Dosya yoluyla OCR Sonucu:")
print(result_file)

print("\nBase64 ile OCR Sonucu:")
print(result_base64)
```