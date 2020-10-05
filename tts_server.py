#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import logging
import os
import subprocess
import sys

try:
    from urllib.parse import urlencode
except ImportError:
    # Probably Python2
    from urllib import urlencode
    

from flask import Flask
from flask import Response
from flask import redirect
from flask import request


version_tuple = (0, 0, 1)
version = version_string = __version__ = '%d.%d.%d' % version_tuple
__author__ = 'clach04'

log = logging.getLogger(__name__)
logging.basicConfig()  # TODO include function name/line numbers in log
log.setLevel(level=logging.DEBUG)  # Debug hack!

log.info('Python %s on %s', sys.version, sys.platform)


class BaseTTS(object):
    pass  # nothing shared yet

class Espeak(BaseTTS):
    """Use eSpeak command line tool http://espeak.sourceforge.net/"""
    def gen_mp3(self, text, lang='en'):
        # uses pipes and stdin/out - does NOT materialize audio files to file system
        argv = ['/usr/bin/espeak', '--stdin', '--stdout', '-v', lang]  # TODO hard coded path
        if not text.endswith("\n"):
            text = text + "\n"

        try:
            proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        except Exception as e:
            log.warn("Cannot create espeak pipe: %s" % e)
            return None

        try:
            proc_ffmpeg = subprocess.Popen(['ffmpeg', '-i', '-', '-f', 'mp3', '-'], stdin=proc.stdout, stdout=subprocess.PIPE, close_fds=True)
        except Exception as e:
            log.warn("Cannot create ffmpeg pipe: %s" % e)
            return None

        try:
            proc.stdin.write(text.encode('utf-8'))
        except IOError as e:
            log.warn("Cannot write to pipe: errno %d" % (e.errno))
            return None
        except Exception as e:
            log.warn("Cannot write to pipe: %s" % e)
            return None

        proc.stdin.close()
        proc.wait()
        print('pre communicate')
        stdout_data, stderr_data = proc_ffmpeg.communicate()  # add timeout?
        print('post communicate')
        print(stderr_data)
        print(len(stdout_data))
        print(type(stdout_data))
        # TODO read it back :-)
        return stdout_data


    def gen_wave(self, text, lang='en'):
        # dupes alot of gen_wave() :-(
        argv = ['/usr/bin/espeak', '--stdin', '--stdout', '-v', lang]  # TODO hard coded path
        if not text.endswith("\n"):
            text = text + "\n"

        try:
            proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        except Exception as e:
            log.warn("Cannot create pipe: %s" % e)
            return None

        try:
            proc.stdin.write(text.encode('utf-8'))
        except IOError as e:
            log.warn("Cannot write to pipe: errno %d" % (e.errno))
            return None
        except Exception as e:
            log.warn("Cannot write to pipe: %s" % e)
            return None

        #proc.stdin.close()
        #proc.wait()
        stdout_data, stderr_data = proc.communicate()  # add timeout?
        print(stderr_data)
        print(len(stdout_data))
        print(type(stdout_data))
        # TODO read it back :-)
        return stdout_data


class GoogleTranslate(BaseTTS):
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
    'espeak': Espeak(),
    'google_translate': GoogleTranslate(),
}

app = Flask(__name__)


# Similar (subset of) https://github.com/synesthesiam/opentts
""" Sample URLs
    'http://127.0.0.1:5000/api/tts?text=no&voice=google_translate:en'
    'http://127.0.0.1:5000/api/tts?text=nein&voice=google_translate:de'
"""
@app.route('/api/tts', methods=['GET'])
def tts():
    voice = request.args.get('voice', 'google_translate:en')
    text = request.args.get('text', 'hey there')  # TODO error if missing
    print(text)
    print(voice)
    voice_split = voice.split(':')
    engine_name = voice_split[0]
    lang = voice_split[1]  # TODO review this...
    engine = engines[engine_name]

    try:
        url = engine.gen_url(text, lang=lang)
        print(url)
        return redirect(url)
    except AttributeError:
        # and/or NotImplemented?

        """
        result = engine.gen_wave(text, lang=lang)
        return Response(result, mimetype='audio/wav')
        """

        result = engine.gen_mp3(text, lang=lang)
        return Response(result, mimetype='audio/mp3')

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

