"""sopel-jisho

Jisho lookup plugin for Sopel IRC bots.

Copyright 2016, dgw
Licensed under the GPL v3.0 or later
"""
from __future__ import annotations

from sopel import plugin

import requests


api_url = 'https://jisho.org/api/v1/search/words?keyword=%s'
request_headers = {
    'User-Agent': 'sopel-jisho (https://github.com/dgw/sopel-jisho)',
}


@plugin.commands('jisho', 'ji')
@plugin.output_prefix('[jisho] ')
@plugin.example('.ji onsen')
def jisho(bot, trigger):
    query = trigger.group(2) or None
    bot.say(fetch_result(query))


def fetch_result(query):
    if not query:
        return "No search query provided."
    try:
        r = requests.get(
            url=api_url % query,
            headers=request_headers,
            timeout=(10.0, 4.0),)
    except requests.exceptions.ConnectTimeout:
        return "Connection timed out."
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to server."
    except requests.exceptions.ReadTimeout:
        return "Server took too long to send data."
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "HTTP error: " + str(e)
    try:
        data = r.json()
    except ValueError:
        return r.content
    if data['meta']['status'] != 200:
        return "Jisho API returned error code %s" % data['meta']['status']

    try:
        entry = data['data'][0]
    except IndexError:
        return "No results."

    word = entry['japanese'][0].get('word') or ''
    furigana = [item['reading'] for item in entry['japanese'] if not word or
                (item.get('word') or query) == word and item.get('reading')]
    readings = ', '.join(furigana) if len(furigana) else ''
    if word and readings:
        readings = " ({readings})".format(readings=readings)
    meaning = ', '.join(entry['senses'][0]['english_definitions'])
    return "{word}{readings}: {meaning}".format(word=word, readings=readings, meaning=meaning)
