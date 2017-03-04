from lxml import html
import inflection
import requests
import pystache
import re
import os

def normalize_name(name):
    return inflection.parameterize(unicode(name), '-')

def normalize_code(code):
    return code.replace('_', '\\')

def should_add(name):
    # we are filtering all skin tone emojis
    # we got separate classes for that
    # return 'skin' not in name

    # TODO does not work well, we use the pregenerated from unicode.org
    return True

def fix_work_dir():
    path = os.path.realpath(os.path.dirname(__file__))
    os.chdir(path)
    return

def run():
    page = requests.get('http://unicode.org/emoji/charts/emoji-list.html')
    tree = html.fromstring(page.content)

    codes = tree.xpath('//td[@class="code"]/*[1]/@name')
    names = tree.xpath('//td[@class="name"]/text()')

    emojis = []
    for code, name in dict(zip(codes, names)).iteritems():
        if should_add(name):
            emojis.append({
                'name': normalize_name(name),
                'code': normalize_code(code)
            })

    for item in ['emojis', 'variables']:
        renderer = pystache.Renderer()
        text_style = renderer.render_path('template/_' + item + '.mustache', {'items': emojis})

        text_file = open('../sass/_' + item + '.scss', 'w')
        text_file.write(text_style)
        text_file.close()

fix_work_dir()
run()
