# -*- coding: utf-8 -*-

from datetime import datetime
import os
import random

from flask import Flask, render_template, request
app = Flask(__name__)


TRANSLATIONS = {
    'YES': {
        'en': 'YES',
        'es': 'SI',
        'de': 'JA',
    },
    'NO': {
        'de': 'NEIN'
    },
}


@app.route("/")
def index():
    is_thursday = datetime.now().isoweekday() == 4
    img = get_image(is_thursday)
    return render_template(
        'index.html',
        **{
            'is_thursday': is_thursday and _('YES') or _('NO'),
            'img': img
        }
    )


def _(string):
    langs = get_languages()
    translated = None
    for lang in langs:
        if translated:
            break
        translated = TRANSLATIONS.get(string, {}).get(lang)
    else:
        translated = string
    return translated


def get_languages():
    lang_header = request.headers.get('accept-language')
    if not lang_header:
        return []
    langs = lang_header.split(',')
    langs = sorted(langs, key=sort_value, reverse=True)
    langs = [lang[:2] for lang in langs]
    return langs


def sort_value(x):
    return float(x.split('=')[1]) if '=' in x else 1


def get_image(is_thursday):
    root = os.path.abspath(os.path.dirname(__file__))
    if is_thursday:
        path = 'static/img/thursday'
    else:
        path = 'static/img/other'

    images = [f for f in os.listdir(os.path.join(root, path))
              if f[-3:] in ['jpg', 'png', 'gif']]

    return '%s/%s' % (path, random.choice(images))

if __name__ == "__main__":
    app.run()
