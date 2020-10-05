# SRTTSS - Second Rate (Text To Speach) TTS Server - REST interface

## Getting Started

If installing/working with a source checkout issue:

    pip install -r requirements.txt


  * google_translate requires internet access.
  * Using eSpeak requires an espeak binary, http://espeak.sourceforge.net/
      * `sudo apt-get install espeak`

Run:

    python tts_server.py

Then open a browser to:

  * http://127.0.0.1:5000/api/tts?text=no
  * http://127.0.0.1:5000/api/tts?text=no&voice=google_translate:en
  * http://127.0.0.1:5000/api/tts?text=nein&voice=google_translate:de
  * http://127.0.0.1:5000/api/tts?text=没有&voice=google_translate:zh-cn
  * http://127.0.0.1:5000/api/tts?text=no&voice=espeak:en
  * http://127.0.0.1:5000/api/tts?text=nein&voice=espeak:de


Curl/wget may not work (curl -L needed for redirects).

    curl 'http://127.0.0.1:5000/api/tts?text=nein&voice=google_translate:de'
    curl 'http://127.0.0.1:5000/api/tts?text=no&voice=espeak:en'


Google Translate emulator - no control over TTS engine used, requires eSpeak:

  * http://127.0.0.1:5000/translate_tts?ttsspeed=1&l=en&q=hello+world&tl=en&client=tw-ob&total=1&ie=UTF-8
  * http://127.0.0.1:5000/translate_tts?l=en&q=hello+world
  * http://127.0.0.1:5000/translate_tts?q=hello+world

Curl/wget does work:

    wget 'http://127.0.0.1:5000/translate_tts?q=hello+world'
    curl 'http://127.0.0.1:5000/translate_tts?q=hello+world'

