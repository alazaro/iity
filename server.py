# -*- coding: utf-8 -*-

from datetime import datetime
import md5
import os
import random

from flask import Flask, render_template, request, redirect, url_for, abort
import pytz
app = Flask(__name__)


img_hash_cache = {
    True: {},
    False: {},
}







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


@app.route("/<img_hash>")
@app.route("/")
def index(img_hash=None):
    if img_hash == 'favicon.ico':
        return abort(404)
    is_thursday = datetime.now(
        pytz.timezone('Europe/Madrid')).isoweekday() == 4
    if not img_hash:
        img_hash, img = get_image(is_thursday)
        return redirect(url_for('index', img_hash=img_hash))

    else:
        img = get_img_from_hash(img_hash, is_thursday)
        return render_template(
            'index.html',
            **{
                'is_thursday': is_thursday and _('YES') or _('NO'),
                'img': img
            }
        )


def get_img_from_hash(img_hash, is_thursday):
    img_path = img_hash_cache[is_thursday].get(
        img_hash, get_image(is_thursday)[1])
    return img_path


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

    img_path = '%s/%s' % (path, random.choice(images))
    img_hash = md5.md5(img_path.decode('utf-8')).hexdigest()[:6]
    img_hash_cache[is_thursday][img_hash] = img_path
    return img_hash, img_path

if __name__ == "__main__":
    app.run()
