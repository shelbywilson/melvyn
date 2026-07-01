import json

def _load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

config                        = _load('./../config/config.json', {'MAX_LENGTH_URL': 100, 'FILE_VERSION': '03'})
episodes_dictionary           = _load('./../data/episodes_dictionary.json', {})
descriptions                  = _load('./../data/bbc_descriptions_short.json', {})
episode_thumbnails            = {
    **_load('./../data/episode_thumbnails.json', {}),
    **_load('./../data/episode_thumbnails_manual.json', {}),
}
categories_by_episode         = _load('./../data/categories_by_episode.json', {})
top_level_categories_by_episode = _load('./../data/top_level_categories_by_episode.json', {})

def div(inner, _class = ""):
    return wrapper('div', inner, _class)

def p(inner, _class = ""):
    return wrapper('p', inner, _class)

def li(inner, _class = ""):
    return wrapper('li', inner, _class)

def a(inner, href, _class = "", blank = True):
    _blank = ''
    if (blank):
        _blank = '_blank'
    return wrapper('a', inner, _class, [{'name': 'target', 'value': _blank}, {'name': 'href', 'value': href}], False)

def wrapper(tag, inner, _class = "", attr = [], newline = True):
    c = ''
    a = ''
    if _class:
        c = ' class="' + _class + '"'
    for at in attr:
        a += ' ' + at['name'] + '="' + at['value'] + '" '
        
    return '<' + tag + c + a + '>' + inner + '</' + tag + '>' + ('\n' if newline else '')

def get_url(key):
    url = key.replace(' ', '_')
    return url[0:config['MAX_LENGTH_URL']]

def get_wiki_img(key):
    wiki_img = ''
    try:
        thumb = episode_thumbnails[key]
        if isinstance(thumb, dict):
            url = thumb.get('url', '')
            w = thumb.get('width')
            h = thumb.get('height')
        else:
            url = thumb
            w = h = None
        if url:
            dims = f' width="{w}" height="{h}"' if w and h else ''
            wiki_img = f'<div><img src="{url}"{dims} /></div>\n'
    except:
        pass
    return wiki_img

def get_description(key):
    return descriptions[episodes_dictionary[key]['date'] + '_' + key]

def get_episode_row(key, this_guest = False):
    try: 
        episode = episodes_dictionary[key]

        if this_guest:
            guest_list = 'Also featuring: '
        else: 
            guest_list = 'Featuring: '
        for expert in episode['experts']:
            if expert['name'] != this_guest:
                guest_list += '<span>' + a(expert['name'], './../guest/' + get_url(expert['name']) + '.html', 'no-wrap', False) + '</span>, '
        guest_list = guest_list[:len(guest_list) - 2]

        categories = ''
        for cat in top_level_categories_by_episode.get(key, []):
            categories += a(cat, './../category/' + get_url(cat) + '.html', '', False)

        for cat in categories_by_episode.get(key, []):
            categories += a(cat, './../category/' + get_url(cat) + '.html', '', False)

        content = (
            p(get_description(key)) 
            + p(episode['date']) 
            + p(a('listen &#8599;', 'https://www.bbc.co.uk/sounds/play/' + episode['episode_link'].split('/').pop())) 
            + p(guest_list)
        )
        wiki_link = '<a href="' + episode['wiki_link'] + '" target="_blank">' + get_wiki_img(key) + '<div>wikipedia article &#8599;</div></a>\n'
        ranking_placeholder = '<div data-topic="' + episode['topic'] + '" class="episode-ranking"><div class="ranking"><div class="flex-row"><div class="progress-bar"><div class="score-60"></div>\n</div>\n<div class="ranking-label">&nbsp;</div>\n</div>\n</div>\n</div>\n'

        return li(
            div('<h3>' + episode['topic'] + '</h3>\n', 'episode-title') 
            + div(div(content, "content-col")
            + div(wiki_link, "wiki-col") 
            + div(ranking_placeholder , "meta-col"), "episode-content"
            ) 
            + div(categories, 'categories')
            , 'episode'
        )
    except:
        print('\tno episode found -', key)
        return ''

def get_related_category_links():
    for category in sorted(set_of_cat, key=sort_by_frequency_category, reverse=True):
        related_html += '<a href="./../category/' + get_url(category) + '.html">' + category + '</a>'

def get_html_page(content, title = "", css = [], js = []):
    meta = ''
    for link in css:
        meta += '<link rel="stylesheet" type="text/css" href="./../client/css/' + link + '.' + config["FILE_VERSION"] + '.css" />\n'
    for link in js:
        meta += '<script src="./../client/' + link + '.' + config["FILE_VERSION"] + '.js"></script>\n'
    attribution = '<footer class="attribution"><p><a href="https://commons.wikimedia.org/wiki/File:Official_portrait_of_Lord_Bragg_crop_2.jpg" target="_blank">Portrait of Lord Bragg</a> by <a href="https://www.parliament.uk/" target="_blank">UK Parliament</a> / Chris McAndrew, <a href="https://creativecommons.org/licenses/by/3.0/" target="_blank">CC BY 3.0</a></p></footer>\n'
    return '''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta http-equiv="Content-Type"content="text/html; charset=UTF-8" />
            ''' + '<link rel="stylesheet" type="text/css" href="./../client/css/common' + '.' + config["FILE_VERSION"] + '.css" />' + meta + '<meta http-equiv="X-UA-Compatible" content="IE=edge" />\n<meta name="viewport" content="width=device-width, initial-scale=1" />\n<meta name="robots" content="index,follow,noai,noimageai" />\n<meta name="googlebot" content="index,follow" />\n<meta property="og:title" content="' + title +'" />\n<meta property="og:description" content="" />\n<meta name="theme-color" content="#000">\n<title>' + title + '</title>\n<link rel="icon" href="./../client/lord-bragg.jpg" />\n</head>\n<body>\n<main>\n' + content + attribution + '</main>\n</body>\n</html>'
