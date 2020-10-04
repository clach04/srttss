#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import sys

try:
    from urllib.parse import urlencode
except ImportError:
    # Probably Python2
    from urllib import urlencode
    

from flask import Flask
from flask import redirect
from flask import request



class BaseTTS(object):
    pass

class Google(BaseTTS):
    """Use google translate TTS interface"""
    def gen_url(self, text, lang='en'):
        print(text)
        print(lang)
        base_url = 'https://translate.google.com/translate_tts?'
        vars = {
            'q': text,
            'l': lang,
            'tl': lang,
            'client': 'tw-ob',
            'ttsspeed': 1,
            'total': 1,
            'ie': 'UTF-8',
            # looks like can get away with out 'textlen'
        }
        result = base_url + urlencode(vars)
        return result

engines = {
    'google': Google(),
}

app = Flask(__name__)


# Similar (subset of) https://github.com/synesthesiam/opentts
""" Sample URLs
    'http://127.0.0.1:5000/api/tts?text=no&voice=google:en'
    'http://127.0.0.1:5000/api/tts?text=nein&voice=google:de'
"""
@app.route('/api/tts', methods=['GET'])
def tts():
    voice = request.args.get('voice', 'google:en')
    text = request.args.get('text', 'hey there')  # TODO error if missing
    print(text)
    print(voice)
    voice_split = voice.split(':')
    engine_name = voice_split[0]
    lang = voice_split[1]  # TODO review this...
    engine = engines[engine_name]

    url = engine.gen_url(text, lang=lang)
    print(url)
    return redirect(url)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print(sys.platform, sys.version)

    settings = {
        #'debug': True,
        'host': '0.0.0.0',
    }
    app.run(**settings)

    return 0


if __name__ == "__main__":
    sys.exit(main())

