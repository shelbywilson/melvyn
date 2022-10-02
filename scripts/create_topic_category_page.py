import json
from html_util import get_html_page, get_url, div, p, a, get_episode_row

def create_topic_category_page():
    print('\n### start create_topic_category_page')
    f = open('./../data/topics_by_category_non_unique.json')
    topics_by_category = json.load(f)
    f.close()

    f = open('./../data/categories_by_episode.json')
    categories_by_episode = json.load(f)
    f.close()

    f = open('./../data/category_summaries.json')
    category_summaries = json.load(f)
    f.close()

    index_html = ''

    def sort_by_len(key):
        return len(topics_by_category[key])

    for key in sorted(topics_by_category.keys(), key=sort_by_len, reverse=True):
        category_html = '<header>' 
        category_html += p(a('&larr; episodes', './../', '', False), 'header-back-link')
        category_html += '<h1>' + key + '</h1>'
    
        try:
            category_html += div(p(category_summaries[key]), "category-summary")
        except:
            pass

        category_html += p(str(len(topics_by_category[key])) + ' episodes')

        episode_list = ''
        related_categories = set()
        for topic in sorted(topics_by_category[key]):
            episode_list += get_episode_row(topic)
            for cat in categories_by_episode[topic]:
                if cat != key:
                    related_categories.add(cat)

        related_html = ''
        for cat in sorted(related_categories, key=sort_by_len, reverse=True):
            related_html += a(cat, './../category/' + get_url(cat) + '.html', '', False)

        category_html += div(related_html, 'categories')
        category_html += '</header>' 

        category_html += '<ol id="episodes">' + episode_list + '</ol>'

        index_html += '<details><summary>' + key + ' (' + str(len(topics_by_category[key])) + ')</summary>' + p(episode_list) + '</details>'

        w = open('./../category/' + get_url(key) + '.html', 'w')
        w.write(get_html_page(category_html, key, ['guest', 'category'], ['util', 'add-episode-scores']))
        w.close()
    
    print('\t', len(topics_by_category.keys()), 'category pages written')

    w = open('./../category/index.html', 'w')
    w.write(get_html_page(index_html, 'episode categories'))
    w.close()

    print('### end create_topic_category_page')

if __name__=="__main__":
    create_topic_category_page()