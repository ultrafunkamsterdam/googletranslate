"""

████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗███████╗
╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝
   ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   █████╗  
   ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██╔══╝  
   ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                                            
UltrafunkAmsterdam
https://github.com/UltrafunkAmsterdam/Translate
v: 1.1

installation:
pip git+https://github.com/ultrafunkamsterdam/Translate

usage:

from translate import translate

translate('some string in english', 'en', 'nl')
translate('some string in english', 'en', 'fr') 

# if you have lots of translations to make use use the Translator class

from translate import Translator
translator = Translator('en', 'jp')
with open(sourcefile) as fh, open(destfile) as fd:  # translates one file to another
  fd.writeline(translator.translate(fh.readline()))

"""
import math
import re
import time
import requests


def translate(text, source_lang, dest_lang):
    return Translator(source_lang, dest_lang).translate(text)


class TranslatedString(str):

    def __new__(cls, *s, extra=None):
        print('__new__', s)
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

    def __init__(self, source_language, destination_language, session=None):
        self.source_language = source_language
        self.destination_language = destination_language
        self._re_tkk = re.compile(r"tkk:\'(.+?)\'", re.DOTALL)
        self._api_url = "https://translate.google.com{}"
        self._session = session or requests.session()
        self._ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " "(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        self._session.headers.update({"user-agent": self._ua})
        self._tkk = ""
        self._last_data = None


    def translate(self, text):
        tk = self._calc_token(text)
        url = self._api_url.format("/translate_a/single")
        params = {
            "client": "webapp",
            "sl": self.source_language,
            "tl": self.destination_language,
            "hl": self.destination_language,
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
            translation += part[0]
        
        self._last_data = raw
        return TranslatedString(translation, extra=raw)



    def _calc_token(self, text):
        if self._tkk:
            now: str = str(int(time.time() / 3600))
            if self._tkk.split(".")[0] == now:
                pass
        else:
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
