import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import re

from .answer import AnswerAPI, DetectedLanguage


URL = "https://libretranslate.com"

boundary = "---------------------------"

cookies = {
    'session': '2d87b697-679c-4375-bcfe-260036e86b42',
    '_ga_KPKM1EP5EW': 'GS1.1.1718127199.3.1.1718127868.0.0.0',
    '_ga': 'GA1.1.143854405.1718028233',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': f'multipart/form-data; boundary={boundary}',
    'Origin': URL,
    'Alt-Used': 'libretranslate.com',
    'Connection': 'keep-alive',
    'Referer': URL,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}



def __get_secret() -> str:
    resp = requests.get(URL + "/js/app.js")
    unclean_secret = re.search(r"apiSecret: \"\w{7}\"", resp.text)[0]

    secret = unclean_secret.split("\"")[1]
    return secret


def translate(
        query: str, 
        source_lang: str = "auto", 
        target_lang: str = "ru", 
        alternatives: int = 0, 
        ) -> AnswerAPI:

    data = MultipartEncoder({
        'q': query,
        'source': source_lang,
        'target': target_lang,
        'format': "text",
        'alternatives': str(alternatives),
        'api_key': "",
        'secret': __get_secret(),
    }, boundary=boundary)

    resp = requests.post(URL + '/translate', cookies=cookies, headers=headers, data=data.to_string())
    data = resp.json()

    detected_language = None
    if source_lang == "auto":
        detected_language = DetectedLanguage(
            data["detectedLanguage"]["confidence"],
            data["detectedLanguage"]["language"],
        )

    return AnswerAPI(
        data.get("translatedText", ""),
        data.get("alternatives", []),
        detected_language
    )
