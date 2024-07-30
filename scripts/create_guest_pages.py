import json
from html_util import get_url, get_html_page, div, get_episode_row

def create_guest_pages():
    print('\n### start create_guest_pages')
    f = open('./../data/guest_frequency.json')
    frequency = json.load(f)
    f.close()

    def sort_by_count(name):
        return frequency[name]['count']

    f = open('./../data/topics_by_guest.json')
    topics_by_guest = json.load(f)
    f.close()

    f = open('./../data/categories_by_episode.json')
    categories_by_episode = json.load(f)
    f.close()

    f = open('./../data/topics_by_category_non_unique.json')
    topics_by_category_non_unique = json.load(f)
    f.close()

    def sort_by_frequency_category(key):
        return len(topics_by_category_non_unique[key])

    for guest in frequency.keys():
        el = frequency[guest].copy()
        el['name'] = guest
        curr_title = frequency[guest]['title'][0]

        # start header
        guest_html = '<header>'
        guest_html += '<p class="header-back-link" ><a href="./../">&larr; episodes</a></p>'
        # guest_html += '<p class="header-back-link" ><a href="./../guest/index.html">&larr; guests</a></p>'

        # add name
        guest_html += '<h1>' + guest + '</h1>'

        # add title
        guest_html += '<p class="mt-0"><em>' + curr_title + '</em></p>'
        try:
            if el['links'][0]['text'] == guest:
                guest_html += '<p><a href="' + el['links'][0]['wiki'] + '" target="_blank">wikipedia &#8599;</a></p>'
        except: 
            pass
            # print('\t--- no wiki link ', guest)
        guest_html += '</p>'

        # add set of categories
        set_of_cat = []
        for episode in topics_by_guest[guest]:
            try:
                for category in categories_by_episode[episode['topic']]:
                    # categories_by_episode_html += '<a href="./../category/' + category.replace(' ', '_') + '.html">' + category + '</a>'
                    if category not in set_of_cat:
                        set_of_cat.append(category)
            except:
                pass
                
        # add episode count
        count = frequency[guest]['count']
        if count != 1:
            count_label = ' episodes'
        else:
            count_label = ' episode'
        guest_html += '<p class="mb-0">' + str(frequency[guest]['count']) + count_label + '</p>'

        # add related categories
        related_html = ''

        for category in sorted(set_of_cat, key=sort_by_frequency_category, reverse=True):
            related_html += '<a href="./../category/' + get_url(category) + '.html">' + category + '</a>'

        if (len(set_of_cat) > 0):
            guest_html += '<p style="margin-bottom: -1rem">Covers topics in categories such as:</p>'

        guest_html += div(related_html, 'categories')

        # end header
        guest_html += '</header>'

        # add episodes
        guest_html += '<ol id="episodes">'
        for episode in topics_by_guest[guest]:
            guest_html += get_episode_row(episode['topic'], guest)
        guest_html += '</ol>'
        
        w = open('./../guest/' + get_url(guest) + '.html', 'w')
        w.write(get_html_page(guest_html, guest, ['guest'], ['util', 'add-episode-scores']))
        w.close()
    
    print('\t', len(topics_by_guest.keys()), 'guest pages written')

    # begin all guests page
    index_html = '<header><p class="header-back-link"><a href="./../">&larr; episodes</a></p><h1>All guests</h1></header>'
    index_html += '<ul>'
    for guest in sorted(sorted(frequency.keys()), key=sort_by_count, reverse=True):
        index_html += '<li>'
        index_html += '<div class="flex-row space-between">'
        index_html += '<div><a href="./../guest/' + guest.replace(' ', '_') + '.html">' + guest + '</a><div><em>' + frequency[guest]['title'][0] + '</em></div></div><div class="text-right"><div class="no-wrap">' + frequency[guest]['last'] + '</div>' 
        if frequency[guest]['last'] != frequency[guest]['first']:
            index_html += '<div class="no-wrap">' + frequency[guest]['first'] + '</div>'
        index_html += '</div>'
        index_html += '</div>'
        index_html += '<details>'
        index_html += '<summary>' + str(frequency[guest]['count']) + ' episodes </summary>'
        index_html += '<ul>'
        for topic in topics_by_guest[guest]:
            index_html += '<li>' + topic['topic'] + '</li>'
        index_html += '</ul>'
        index_html += '</details>'
        index_html += '</li>'

    index_html += '</ul>'

    w = open('./../guest/index.html', 'w')
    w.write(get_html_page(index_html, 'all guests', ['guests'], ['util.js']))
    w.close()

    print('### end create_guest_pages')

if __name__=="__main__":
    create_guest_pages()