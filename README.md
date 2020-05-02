```

 ████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗███████╗
 ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝
    ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   █████╗
    ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██╔══╝
    ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ███████╗
    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
```

 UltrafunkAmsterdam
 
 Google translate "without" limits and without API key
 
## installation ##
pip3 install git+https://github.com/ultrafunkamsterdam/googletranslate

## usage: ##
 
```python
 
from translator import translate

>>> translate( 'Have fun using this!', 'auto', 'nl')
'Veel plezier ermee!'

>>> translate( 'Have fun using this!', 'auto', 'fr')
'Amusez-vous en utilisant cela!'

>>> translate( 'Have fun using this!', 'auto', 'de')
'Viel Spaß damit!'


# usage variation 1

>>> from translator import Translator
>>> to_japanese = Translator('auto','ja')
>>> print('lets do something japanese...', to_japanese('Good afternoon!'))
lets do something japanese... こんにちは！


# usage variation 2 : translate files

>>> from translate import Translator
>>> translator = Translator('en', 'jp')
>>> with open(sourcefile, 'r') as infile, open(destfile, 'w+') as outfile:
        # i recommend writing a custom function which translates bigger chunks to minimize the amount of api calls.
        while line := iter(lambda:infile.readline(), ''):
            outfile.writeline(translator(line))
```


