import json

f = open('./../config/config.json')
config = json.load(f)
f.close()

f = open('./../data/episodes_dictionary.json')
episodes_dictionary = json.load(f)
f.close()

f = open('./../data/bbc_descriptions_short.json')
descriptions = json.load(f)
f.close()

f = open('./../data/episode_thumbnails.json')
episode_thumbnails = json.load(f)
f.close()

f = open('./../data/categories_by_episode.json')
categories_by_episode = json.load(f)
f.close()

f = open('./../data/top_level_categories_by_episode.json')
top_level_categories_by_episode = json.load(f)
f.close()

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
        if episode_thumbnails[key] != "":
            wiki_img = '<div><img src="' + episode_thumbnails[key] + '" /></div>\n'
    except:
        pass
    return wiki_img

def get_description(key):
    return descriptions[episodes_dictionary[key]['date'] + '_' + key]

def get_episode_row(key, this_guest = False):
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
    try:
        for cat in top_level_categories_by_episode[key]:
            categories += a(cat, './../category/' + get_url(cat) + '.html', '', False)
    except:
        pass

    for cat in categories_by_episode[key]:
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

def get_related_category_links():
    for category in sorted(set_of_cat, key=sort_by_frequency_category, reverse=True):
        related_html += '<a href="./../category/' + get_url(category) + '.html">' + category + '</a>'

def get_html_page(content, title = "", css = [], js = []):
    meta = ''
    for link in css:
        meta += '<link rel="stylesheet" type="text/css" href="./../client/css/' + link + '.' + config["FILE_VERSION"] + '.css" />\n'
    for link in js:
        meta += '<script src="./../client/' + link + '.' + config["FILE_VERSION"] + '.js"></script>\n'
    return '''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta http-equiv="Content-Type"content="text/html; charset=UTF-8" />
            ''' + '<link rel="stylesheet" type="text/css" href="./../client/css/common' + '.' + config["FILE_VERSION"] + '.css" />' + meta + '<meta http-equiv="X-UA-Compatible" content="IE=edge" />\n<meta name="viewport" content="width=device-width, initial-scale=1" />\n<meta name="robots" content="index,follow" />\n<meta name="googlebot" content="index,follow" />\n<meta property="og:title" content="' + title +'" />\n<meta property="og:description" content="" />\n<meta name="theme-color" content="#000">\n<title>' + title + '</title>\n<link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Official_portrait_of_Lord_Bragg_crop_2.jpg/440px-Official_portrait_of_Lord_Bragg_crop_2.jpg" />\n</head>\n<body>\n<main>\n' + content + '</main>\n</body>\n</html>'