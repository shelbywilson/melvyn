import json
from html_util import get_html_page, get_url, div, li, p, a

def create_topic_category_page():
    print('\n### start create_topic_category_page')
    f = open('./../data/topics_by_category_non_unique.json')
    topics_by_category = json.load(f)
    f.close()

    f = open('./../data/categories_by_episode.json')
    categories_by_episode = json.load(f)
    f.close()

    f = open('./../data/episodes_dictionary.json')
    episodes_dictionary = json.load(f)
    f.close()

    f = open('./../data/episode_thumbnails.json')
    thumbnails = json.load(f)
    f.close()

    f = open('./../data/bbc_descriptions_short.json')
    descriptions = json.load(f)
    f.close()

    f = open('./../data/category_summaries.json')
    category_summaries = json.load(f)
    f.close()

    index_html = ''

    def sort_by_len(key):
        return len(topics_by_category[key])

    for key in sorted(topics_by_category.keys(), key=sort_by_len, reverse=True):
        category_html = p(a('&larr; episodes', './../', '', False), 'header-back-link')
        category_html += '<h1>' + key + '</h1>'
    
        try:
            category_html += div(p(category_summaries[key]), "category-summary")
        except:
            pass

        category_html += p(str(len(topics_by_category[key])) + ' episodes')

        episode_list = ''
        related_categories = set()
        for episode in sorted(topics_by_category[key]):
            episode_list += li(
                div(
                    '<h3 class="">' + episode + '</h3>' 
                    + div(
                        div(
                            p(descriptions[episodes_dictionary[episode]['date'] + '_' + episode]) + p(episodes_dictionary[episode]['date']) 
                            + p(a('listen &#8599;', 'https://www.bbc.co.uk/sounds/play/' + episodes_dictionary[episode]['episode_link'].split('/').pop(), 'content-col'))
                        , 'content-col') 
                        + div('<img src="' + thumbnails[episode] + '" />', 'wiki-col')
                        # + div('&nbsp;', 'meta-col')
                    , 'episode-content')
                ) 
            )
            for cat in categories_by_episode[episode]:
                if cat != key:
                    related_categories.add(cat)

        related_html = ''
        for cat in sorted(related_categories, key=sort_by_len, reverse=True):
            related_html += a(cat, './../category/' + get_url( get_url(cat)) + '.html', '', False)

        category_html += '<ol>' + episode_list + '</ol>'
        category_html += div(related_html, 'categories')

        index_html += '<details><summary>' + key + ' (' + str(len(topics_by_category[key])) + ')</summary>' + p(episode_list) + '</details>'

        w = open('./../category/' + get_url(key) + '.html', 'w')
        w.write(get_html_page(category_html, key, ['guest.01', 'category.01']))
        w.close()
    
    print('\t', len(topics_by_category.keys()), 'category pages written')

    w = open('./../category/index.html', 'w')
    w.write(get_html_page(index_html, 'episode categories'))
    w.close()

    print('### end create_topic_category_page')

if __name__=="__main__":
    create_topic_category_page()