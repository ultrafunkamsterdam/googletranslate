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
 
>>>from googletranslate import translate

>>> translate( 'Have fun using this!', 'nl')
'Veel plezier ermee!'

# you could also explicitly specify source and/or destination language.
>>> translate( 'have fun using this', dest='nl',  src='en' )

>>> translate( 'Have fun using this!', 'fr')
'Amusez-vous en utilisant cela!'

>>> translate( 'Have fun using this!', 'de', 'en')
'Viel Spaß damit!'


# usage variation 1

>>> from googletranslate import Translator
>>> to_japanese = Translator('ja')
>>> print('lets do something japanese...', to_japanese('Good afternoon!'))
lets do something japanese... こんにちは！


# usage variation 2 : translate files

>>> from googletranslate import Translator
>>> translator = Translator('es')
>>> with open(somedocument.txt, 'r') as infile, open(somespanishdocument.txt, 'w+') as outfile:
        # i recommend writing a custom function which translates bigger chunks to minimize the amount of api calls.
        for line in infile:
            outfile.write(translator(line))
```


