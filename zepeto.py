import requests
from PIL import Image

API_HOST = '47.74.149.35/api'
PHOTOBOOTH_ID = '14H8320f7MYeqkg0UEwmGY'  # PHOTOBOOTH_ONE_87
HASHCODE = '1VREP0'
# HASHCODE = 'MD92C6'
URL = f'http://{API_HOST}/photo/{PHOTOBOOTH_ID}/?hashCodes={HASHCODE}&width=500'

def main():
    filename = './mask.png'

    print(URL)
    res = requests.get(URL)
    if res.status_code == 200:
        with open(filename, 'wb') as mask_file:
            for chunk in res:
                mask_file.write(chunk)

    original = Image.open(filename)

    left, top, right, bottom = 125, 20, 375, 305
    face = original.crop((left, top, right, bottom))
    face.save(filename)

if __name__ == '__main__':
    main()
