from bs4 import BeautifulSoup
import urllib.request
import json

def get_thumbnails():
    f = open('./../data/episodes.json')
    episodes = json.load(f)
    f.close()

    f = open('./../data/episode_thumbnails.json')
    dictionary = json.load(f)
    f.close()

    for episode in episodes:
        if (episode['wiki_link'] != ""):
            if (not episode['topic'] in dictionary):
                print(episode['wiki_link'])
                html_page = urllib.request.urlopen(episode['wiki_link'])
                soup = BeautifulSoup(html_page, "html.parser")
                try:
                    thumb = soup.find('td', {'class': "infobox-image"}).find('img')['src']
                    # print('\tinfobox')
                except:
                    try:
                        thumb = soup.find('div', {'class': "thumb"}).find('img')['src']
                        # print('\tthumb')
                    except:
                        try:
                            thumb = soup.find('table', {'class': "sidebar"}).find('img')['src']
                            # print('\tsidebar')
                        except:
                            # print('\tnot found')
                            thumb = ''
                dictionary[episode['topic']] = thumb
            # else:
            #     print('skip', episode['topic'])
        else:
            print('\t--', 'no image', episode['topic'])

    w = open('./../data/episode_thumbnails.json', 'w')
    json.dump(dictionary, w, indent=4, ensure_ascii=False)
    w.close()