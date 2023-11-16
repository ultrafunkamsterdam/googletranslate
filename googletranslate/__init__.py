"""

 ████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗███████╗
 ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝
    ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   █████╗
    ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██╔══╝
    ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ███████╗
    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝

 UltrafunkAmsterdam
 v: 2.0

 Google translate "without" limits and without API key


 usage:
 from googletranslate import translate

 translate( 'Have fun using this!', 'nl')
 'Veel plezier ermee!'

 translate( 'Have fun using this!', 'fr')
 'Amusez-vous en utilisant cela!'

 translate( 'Have fun using this!', 'de', 'en') # this seocond parameter to specify source language - 'auto' by default.
 'Viel Spaß damit!'



 # usage variation 1

 from googletranslate import Translator
 to_japanese = Translator('ja','auto')
 print('lets do something japanese...', to_japanese('Good afternoon!'))

 lets do something japanese... こんにちは！



 # usage variation 2 : translate files

 from googletranslate import Translator
 translator = Translator('en', 'jp')

 # of course you can also translate a complete file if it does not exceed 5000 characters.

 with open(sourcefile, 'r') as srcf, open(destfile, 'w+') as dstf:
     # i recommend writing a custom function which translates bigger chunks to minimize the amount of api calls.
     while line := iter(lambda:fh.readline(), ''):
        dstf.writeline(translator.translate(line)

"""

__version__  = '2.0'
__author__   = 'Leon van Goolen - UltrafunkAmsterdam'
__license__  = 'MIT'
__version__  = '2.0.0'
__status__   = 'Development'

__all__ = ['translate', 'Translator', 'LANG_CODE_TO_NAME', 'LANG_NAME_TO_CODE']

import math
import re
import time
import logging
import requests

logger = logging.getLogger(__name__)

LANG_CODE_TO_NAME = {
    "auto": "auto-recognized",
    "nl": "Dutch",
    "fy": "Frisian",
    "en": "English",
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "eb": "Cebuano",
    "ny": "Chichewa",
    "CN": "Chinese (Simplified)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "aw": "Hawaiian",
    "iw": "Hebrew",
    "hi": "Hindi",
    "mn": "Mongolian",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "ko": "Korean",
    "ku": "Kurdish (Kurmanji)",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "no": "Norwegian",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu",
    "TW": "Chinese (Traditional)",
}
LANG_NAME_TO_CODE = dict(map(reversed, LANG_CODE_TO_NAME.items()))


def translate(
    text,
    dest,
    src="auto",
):
    return Translator(dest, src).translate(text)


class TranslatedString(str):
    def __new__(cls, s, extra=None):
        return super().__new__(cls, s)

    def __init__(self, s, extra=None):
        super().__init__()
        if isinstance(extra, str):
            self.detected_language = extra
         
        response_parts_name_mapping = {
            0: "translation",
            1: "all-translations",
            2: "original-language",
            5: "possible-translations",
            6: "confidence",
            7: "possible-mistakes",
            8: "language",
            11: "synonyms",
            12: "definitions",
            13: "examples",
            14: "see-also",
        }

        self.extra = {}
        if extra:
            for index, category in response_parts_name_mapping.items():
                self.extra[category] = (
                    extra[index] if (index < len(extra) and extra[index]) else ""
                )


class Translator(object):
    _ua = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1_4) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Mobile/16D57"
    )

    _api_url = "https://translate.googleapis.com{}"

    def __init__(self, destination_language=None, source_language="auto", session=None):

        if not destination_language:
            raise KeyError("missing destination language")
        if not source_language:
            source_language = "auto"
        self.source_language = source_language
        self.destination_language = destination_language
        self._re_tkk = re.compile(r"tkk=\'(.+?)\'", re.DOTALL)
        self._session = session or requests.session()
        self._session.headers.update({"user-agent": self._ua})
        self.__class__._tkk = ""
        self._last_data = None
        self._last_response = None
        self._last_request = None

    def __call__(self, text):
        return self.translate(text)

    def _call(self, url, **kw):
        r = self._last_response = self._session.get(url, params=kw)
        self._last_request = self._last_response.request
        return r

    def translate(self, text: str):
        """translates  <text> to configured destination_language"""
        tk = self._calc_token(text)
        url = self._api_url.format("/translate_a/t")

        params = {
            "anno": "3",
            "client": "t",
            "format": "html",
            "v": 1.0,
            "key": None,
            "logld": "vTE_20200506_00",
            "sl": self.source_language,
            "tl": self.destination_language,
            "sp": "nmt",
            "tc": 1,
            "sr": 1,
            "tk": tk,
            "mode": 1,
            "q": text,
        }
     
        def unwield(arr):
            """
            unwield structure consisting of lists of lists
            to extract the translated string.
            does not modify the passed array in place
            """
            c = arr[:]
            while isinstance(c, list) and len(c) >= 1:
                c = c[0]
            return c
         
        r = self._call(url, **params)
        logger.debug('response: %s => %s' % (r, r.text))
        raw = r.json()
        self._last_data = raw
                
        if not raw:
            return TranslatedString("")
        self._last_data = raw
        
        if not isinstance(raw, str):
            raw = unwield(raw)
       
        if '<b>' in raw:
            raw = ''.join(re.findall(r'<b>(.*?)</b>', raw))

        return TranslatedString(raw)
        

    def _calc_token(self, text):

        if (
            not self.__class__._tkk
            or int(self.__class__._tkk.split(".")[0]) < int(time.time() / 3600) - 18000
        ):
            logger.debug("generating new tkk")
            # just calling it to simulate human behaviour (as far as possible)
            self._session.get(
                self._api_url.format(
                    "/translate_a/l?client=t&alpha=true&hl=en&cb=callback"
                )
            )

            r = self._session.get(
                self._api_url.format(
                    "/translate_a/element.js?cb=googleTranslateElementInit"
                )
            )
            self.__class__._tkk = self._re_tkk.search(r.text)[1]

        def xor_rot(a, b):
            size_b = len(b)
            c = 0
            while c < size_b - 2:
                d = b[c + 2]
                d = ord(d[0]) - 87 if "a" <= d else int(d)
                d = (a % 0x100000000) >> d if "+" == b[c + 1] else a << d
                a = a + d & 4294967295 if "+" == b[c] else a ^ d
                c += 3
            return a

        a = []
        for i in text:
            val = ord(i)
            if val < 0x10000:
                a += [val]
            else:
                a += [
                    math.floor((val - 0x10000) / 0x400 + 0xD800),
                    math.floor((val - 0x10000) % 0x400 + 0xDC00),
                ]
        b = self.__class__._tkk if self.__class__._tkk != "0" else ""
        d = b.split(".")
        b = int(d[0]) if len(d) > 1 else 0
        e = []
        g = 0
        size = len(text)
        while g < size:
            l = a[g]
            if l < 128:
                e.append(l)
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    if (
                        (l & 64512) == 55296
                        and g + 1 < size
                        and a[g + 1] & 64512 == 56320
                    ):
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + (a[g] & 1023)
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
            g += 1
        a = b
        for i, value in enumerate(e):
            a += value
            a = xor_rot(a, "+-a^+6")
        a = xor_rot(a, "+-3^+b+-f")
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:
            a = (a & 2147483647) + 2147483648
        a %= 1000000
        return "{}.{}".format(a, a ^ b)

    def __repr__(self):
        return f'<{self.__class__.__name__} from "{LANG_CODE_TO_NAME[self.source_language]}" to "{LANG_CODE_TO_NAME[self.destination_language]}">'
