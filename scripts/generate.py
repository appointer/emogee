from lxml import html
import inflection
import requests
import pystache
import re
import os

def parse(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    emojis = {}
    current_group = None
    current_subgroup = None

    table = tree.xpath('//table[@border="1"]/tr')
    for item in table:
        group = item.xpath('th[@class="bighead"]/*[1]/text()')
        if (len(group) > 0):
            current_group = normalize_name(group.pop())
            emojis[current_group] = {}

        subgroup = item.xpath('th[@class="mediumhead"]/*[1]/text()')
        if (len(subgroup) > 0):
            current_subgroup = normalize_name(subgroup.pop())
            emojis[current_group][current_subgroup] = []

        names = item.xpath('td[@class="name"]/text()')
        codes = item.xpath('td[@class="code"]/*[1]/@name')

        for code, name in dict(zip(codes, names)).iteritems():
            emojis[current_group][current_subgroup].append({
                'name': normalize_name(name),
                'code': normalize_code(code)
            })

    return emojis


def write(emojis):
    renderer = pystache.Renderer()

    # global include files
    filename = '../sass/emojis/_all.scss'
    items = map(lambda x: x + '/all', emojis.keys())
    save_template(renderer, filename, 'template/_imports.mustache', items)

    # group include files
    for group, tree in emojis.iteritems():
        filename = '../sass/emojis/' + normalize_name(group) + '/_all.scss'
        save_template(renderer, filename, 'template/_imports.mustache', tree.keys())

        # subgroup emojis
        for subgroup, items in tree.iteritems():
            filename = '../sass/emojis/' + normalize_name(group) + '/_' + normalize_name(subgroup) + '.scss'
            save_template(renderer, filename, 'template/_emojis.mustache', items)


def save_template(renderer, filename, template, items):
    template_text = renderer.render_path(template, {'items': items})

    text_file = create_file(filename)
    text_file.write(template_text)
    text_file.close()


def create_file(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    return open(filename, 'w')

def normalize_name(name):
    return inflection.parameterize(unicode(name), '-')


def normalize_code(code):
    return code.replace('_', '\\')


def fix_work_dir():
    path = os.path.realpath(os.path.dirname(__file__))
    os.chdir(path)


def run():
    emojis = parse('http://unicode.org/emoji/charts/emoji-list.html')
    write(emojis)


fix_work_dir()
run()
