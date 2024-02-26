# SRTTSS - Second Rate (Text To Speech) TTS Server - REST interface

## Getting Started

If installing/working with a source checkout issue:

    pip install -r requirements.txt


  * google_translate requires internet access.
  * Using eSpeak requires an espeak (compatible) binary, http://espeak.sourceforge.net/ and/or https://github.com/espeak-ng/espeak-ng
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
  * Non-standard extension:
      * http://127.0.0.1:5000/translate_tts?q=hello+world&srttss_mimetype=audio/mp3
      * http://127.0.0.1:5000/translate_tts?q=hello+world&srttss_mimetype=audio/wav

Curl/wget does work:

    wget 'http://127.0.0.1:5000/translate_tts?q=hello+world'
    curl 'http://127.0.0.1:5000/translate_tts?q=hello+world'


## What can this be used for?

What ever you want or can think of (hopefully for good rather than evil...).

One use case is as an output target for https://github.com/mqtt-tools/mqttwarn/blob/main/docs/notifier-catalog.md#chromecast

Also see client https://github.com/clach04/tts_client

## Future ideas

  * Implement caching
  * support new/additional backend engines https://github.com/clach04/srttss/issues/1
      * https://github.com/rhasspy/piper https://github.com/rhasspy/larynx command line or http (and/or other MaryTTS compatible servers)

