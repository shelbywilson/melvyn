from bs4 import BeautifulSoup
import urllib.request
import json
# from util import parse_page

def get_bbc_descriptions():
    print('\n### start get_bbc_descriptions')
    f = open('./../data/episodes.json')
    data = json.load(f)
    f.close()

    f = open('./../data/bbc_descriptions.json')
    descriptions = json.load(f)
    f.close()

    new_count = 0

    for episode in data:
        key = episode['date'] + '_' + episode['topic']
        if (not key in descriptions.keys()):
            if (not 'episodes' in episode['episode_link']):
                new_count += 1
                html_page = urllib.request.urlopen('https://www.bbc.co.uk/programmes/' + episode['episode_link'].split('/').pop())
                soup = BeautifulSoup(html_page, "html.parser")
                short_desc = ''
                long_desc = ''

                print('\tnew ', episode['topic'])
                try:
                    short_desc = soup.find('div', {'class': "synopsis-toggle__short"}).find('p').get_text()
                except:
                    print('\tcannot find short description', episode['episode_link'])

                try:
                    long_desc = soup.find('div', {'class': "synopsis-toggle__long"}).get_text()
                except:
                    print('\tcannot find long description', episode['episode_link'])

                descriptions[key] = { 'short_desc': short_desc, 'long_desc': long_desc}
        else:
            pass
            # print('\tskip description', episode['topic'])
    print('\t', new_count, 'new episode descriptions')

    w = open('./../data/bbc_descriptions.json', 'w')
    json.dump(descriptions, w, indent=4, ensure_ascii=False)
    w.close()

    short_descriptions = {}
    for key in descriptions.keys():
        short_descriptions[key] = descriptions[key]['short_desc']

    w = open('./../data/bbc_descriptions_short.json', 'w')
    json.dump(short_descriptions, w, indent=4, ensure_ascii=False)
    w.close()

if __name__=="__main__":
    get_bbc_descriptions()
