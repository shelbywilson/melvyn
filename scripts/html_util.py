import json
f = open('./../config/config.json')
config = json.load(f)
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
    return wrapper('a', inner, _class, [{'name': 'target', 'value': _blank}, {'name': 'href', 'value': href}])

def wrapper(tag, inner, _class = "", attr = []):
    c = ''
    a = ''
    if _class:
        c = ' class="' + _class + '"'
    for at in attr:
        a += ' ' + at['name'] + '="' + at['value'] + '" '
        
    return '<' + tag + c + a + '>' + inner + '</' + tag + '>'

def get_url(key):
    url = key.replace(' ', '_')
    return url[0:config['MAX_LENGTH_URL']]

def get_html_page(content, title = "", css = [], js = []):
    meta = ''
    for link in css:
        meta += '<link rel="stylesheet" type="text/css" href="./../client/css/' + link + '.css" />'
    for link in js:
        meta += '<script src="./../client/' + link + '.js"></script>'
    return '<!DOCTYPE html><html lang="en"><head><meta http-equiv="Content-Type"content="text/html; charset=UTF-8" /><link rel="stylesheet" type="text/css" href="./../client/css/common.01.css" />' + meta + '<meta http-equiv="X-UA-Compatible" content="IE=edge" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="robots" content="index,follow" /><meta name="googlebot" content="index,follow" /><meta property="og:title" content="' + title +'" /><meta property="og:description" content="" /><meta name="theme-color" content="#000"><title>' + title + '</title><link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Official_portrait_of_Lord_Bragg_crop_2.jpg/440px-Official_portrait_of_Lord_Bragg_crop_2.jpg" /></head><body><main>' + content + '</main></body></html>'