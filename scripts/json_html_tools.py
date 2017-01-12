# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 14:22:58 2017

@author: emg
"""

from bs4 import BeautifulSoup

def json_to_html(json):
    data = json['data']['content_html']
    soup = BeautifulSoup(data)
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    html = BeautifulSoup(text)
    return html

def tag_text(html, tagname):
    text = []
    for tag in html.findAll(tagname):
        text.append(tag.text)
    return text