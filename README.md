

 ████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗███████╗
 ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝
    ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   █████╗
    ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██╔══╝
    ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ███████╗
    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
    
 UltrafunkAmsterdam
 
 Google translate "without" limits and without API key
 
 
## usage: ##
 
```python
from translator import translate
translate( 'Have fun using this!', 'auto', 'nl')
'Veel plezier ermee!'
translate( 'Have fun using this!', 'auto', 'fr')
'Amusez-vous en utilisant cela!'
translate( 'Have fun using this!', 'auto', 'de')
'Viel Spaß damit!'
# usage variation 1
from translator import Translator
to_japanese = Translator('auto','ja')
print('lets do something japanese...', to_japanese('Good afternoon!'))
lets do something japanese... こんにちは！
# usage variation 2 : translate files
 
 from translate import Translator
 translator = Translator('en', 'jp')
 with open(sourcefile, 'r') as srcf, open(destfile, 'w+') as dstf:
     dstf.writeline(translator.translate(srcf.readline()))
 ```
