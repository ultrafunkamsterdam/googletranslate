"""

 ████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗███████╗
 ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝
    ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   █████╗
    ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██╔══╝
    ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ███████╗
    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝

 UltrafunkAmsterdam
 v: 1.2

 Google translate "without" limits and without API key


 usage:
 from googletranslate import translate

 translate( 'Have fun using this!', 'auto', 'nl')
 'Veel plezier ermee!'

 translate( 'Have fun using this!', 'auto', 'fr')
 'Amusez-vous en utilisant cela!'

 translate( 'Have fun using this!', 'auto', 'de')
 'Viel Spaß damit!'



 # usage variation 1

 from googletranslate import Translator
 to_japanese = Translator('auto','ja')
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

import math
import re
import time

import requests

LANG_CODE_TO_NAME = {
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
    "TW": "Chinese (Traditional)" ,
}
LANG_NAME_TO_CODE = dict(map(reversed, LANG_CODE_TO_NAME.items()))


def translate(text, from_lang='auto', to_lang=None, ):
    return Translator(from_lang, to_lang).translate(text)


class TranslatedString(str):

    def __new__(cls, *s, extra=None):

        return super().__new__(cls, ''.join(s))

    def __init__(self, *s, extra=None):
        super().__init__()

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


    _ua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
           "AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/75.0.3770.142 Safari/537.36")
    _api_url = "https://translate.google.com{}"


    def __init__(self,
                 source_language='auto',
                 destination_language=None,
                 session=None):

        if not destination_language:
            raise KeyError('missing destination language')

        self.source_language = source_language
        self.destination_language = destination_language

        self._re_tkk = re.compile(r"tkk:\'(.+?)\'", re.DOTALL)

        self._session = session or requests.session()
        self._session.headers.update({"user-agent": self._ua})
        self._tkk = ""
        self._last_data = None

    def __call__(self, text):
        return self.translate(text)

    def translate(self, text: str):
        tk = self._calc_token(text)
        url = self._api_url.format("/translate_a/single")
        params = {
            "client": "webapp",
            "sl": self.source_language,
            "tl": self.destination_language,
            "hl": self.source_language,
            "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],
            "ie": "UTF-8",
            "oe": "UTF-8",
            "otf": 1,
            "ssel": 0,
            "tsel": 0,
            "tk": tk,
            "q": text,
        }
        r = self._session.get(url, params=params)

        raw = r.json()
        result = raw[0]

        if not result:
            return TranslatedString('')
        translation = ''
        for part in result:
            try:
                translation += part[0]
            except:
                continue

        self._last_data = raw
        return TranslatedString(translation, extra=raw)

    def _calc_token(self, text):

        if not self._tkk or self._tkk.split(".")[0] != str(int(time.time() / 3600)):
            r: requests.Response = self._session.get(self._api_url.format(""))
            self._tkk = self._re_tkk.search(r.text)[1]

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
        b = self._tkk if self._tkk != "0" else ""
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
