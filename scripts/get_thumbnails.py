from bs4 import BeautifulSoup
import urllib.request
import json
import re

def find_img(soup):
    # 1. Infobox always wins
    try:
        return soup.find('td', {'class': 'infobox-image'}).find('img')
    except:
        pass

    # 2. Between article thumbnail (figure[typeof="mw:File/Thumb"]) and sidebar,
    #    use whichever appears first in document order.
    #    Restricting to <figure> excludes navbox span icons (e.g. Emblem-money.svg).
    sidebar = soup.find('table', {'class': 'sidebar'})
    fig = soup.find('figure', attrs={'typeof': 'mw:File/Thumb'})

    if sidebar or fig:
        first = soup.find(lambda tag: tag is sidebar or tag is fig)
        if first is not None:
            img = first.find('img')
            if img:
                return img

    # 3. Any default-size figure
    try:
        return soup.find('figure', {'class': 'mw-default-size'}).find('img')
    except:
        pass
    # 4. Last resort
    try:
        return soup.find('div', {'class': 'thumb'}).find('img')
    except:
        pass
    return None

def ensure_min_width(url, min_width=250):
    if '/thumb/' not in url:
        return url
    base, size_part = url.rsplit('/', 1)
    m = re.match(r'^(\d+)px-(.+)$', size_part)
    if not m or int(m.group(1)) >= min_width:
        return url
    return f'{base}/{min_width}px-{m.group(2)}'

def get_thumbnails(force=False):
    f = open('./../data/episodes.json')
    episodes = json.load(f)
    f.close()

    f = open('./../data/episode_thumbnails.json')
    dictionary = json.load(f)
    f.close()

    # Upgrade any cached sub-250px URLs in place without re-fetching
    for entry in dictionary.values():
        if isinstance(entry, dict) and entry.get('url'):
            upgraded = ensure_min_width(entry['url'])
            if upgraded != entry['url']:
                entry['url'] = upgraded
                entry.pop('width', None)
                entry.pop('height', None)

    for episode in episodes:
        if (episode['wiki_link'] != ""):
            entry = dictionary.get(episode['topic'])
            already_fetched = isinstance(entry, dict) and entry.get('url', '') != ''
            if (force or not already_fetched):
                print(episode['wiki_link'])
                try:
                    req = urllib.request.Request(episode['wiki_link'], headers={'User-Agent': 'Mozilla/5.0'})
                    html_page = urllib.request.urlopen(req, timeout=10)
                    soup = BeautifulSoup(html_page, "html.parser")
                    img_tag = find_img(soup)
                    if img_tag:
                        src = img_tag.get('src', '')
                        if src.startswith('//'):
                            src = 'https:' + src
                        upgraded = ensure_min_width(src)
                        new_entry = {'url': upgraded}
                        if upgraded == src:
                            w = img_tag.get('width')
                            h = img_tag.get('height')
                            if w: new_entry['width'] = int(w)
                            if h: new_entry['height'] = int(h)
                        dictionary[episode['topic']] = new_entry
                    else:
                        dictionary[episode['topic']] = {'url': ''}
                except:
                    print('skip', episode['topic'])
            # else:
            #     print('skip', episode['topic'])
        else:
            print('\t--', 'no image', episode['topic'])

    w = open('./../data/episode_thumbnails.json', 'w')
    json.dump(dictionary, w, indent=4, ensure_ascii=False)
    w.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='Refetch all thumbnails, ignoring cache')
    args = parser.parse_args()
    get_thumbnails(force=args.force)