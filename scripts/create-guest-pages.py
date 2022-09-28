import json

f = open('./../data/guest_frequency.json')
frequency = json.load(f)
f.close()

f = open('./../data/topics_by_guest.json')
topics_by_guest = json.load(f)
f.close()

f = open('./../data/episodes.json')
episodes = json.load(f)
f.close()

f = open('./../data/bbc_descriptions_short.json')
descriptions = json.load(f)
f.close()

f = open('./../data/episode_thumbnails.json')
episode_thumbnails = json.load(f)
f.close()

for guest in frequency.keys():
    el = frequency[guest].copy()
    el['name'] = guest
    curr_title = frequency[guest]['title'][0]

    # start header
    guest_html = '<header>'
    guest_html += '<p class="header-back-link" ><a href="./../">&larr; episodes</a></p>'
    # guest_html += '<p class="header-back-link" ><a href="./../guests/index.html">&larr; guests</a></p>'

    # add name
    guest_html += '<h1>' + guest + '</h1>'

    # add title
    guest_html += '<p class="mt-0"><em>' + curr_title + '</em></p>'
    try:
        if el['links'][0]['text'] == guest:
            guest_html += '<p><a href="' + el['links'][0]['wiki'] + '" target="_blank">wikipedia &nearr;</a></p>'
    except: 
        print('--- no wiki link ', guest)
    guest_html += '</p>'

    # end header
    guest_html += '</header>'

    # add episode count
    count = frequency[guest]['count']
    if count != 1:
        count_label = ' episodes'
    else:
        count_label = ' episode'
    guest_html += '<p class="mb-0 text-right">' + str(frequency[guest]['count']) + count_label + '</p>'

    # add episodes
    guest_html += '<ol>'
    for episode in topics_by_guest[guest]:
        desc = descriptions[episode['date'] + '_' + episode['topic']]
        prev_guest_title = episode['title'] 
        wiki_img = ''
        try:
            if episode_thumbnails[episode['topic']] != "":
                wiki_img = '<div><img src="' + episode_thumbnails[episode['topic']] + '" /></div>'
        except:
            continue
        wiki_link = '<a href="' + episode['wiki_link'] + '" target="_blank">' + wiki_img + '<div>wikipedia article &nearr;</div></a>'
        ranking_placeholder = '<div data-topic="' + episode['topic'] + '" class="episode-ranking"><div class="ranking"><div class="flex-row"><div class="progress-bar"><div class="score-60"></div></div><div class="ranking-label">&nbsp;</div></div></div></div>'
        
        other_guests = ''
        for ep in episodes:
            if (ep['topic'] == episode['topic']):
                for expert in ep['experts']:
                    if expert['name'] != guest:
                        other_guests += '<span><a href="./../guests/' + expert['name'].replace(' ', '_') + '.html">' + expert['name'] + '</a></span>, '
                break
        
        other_guests = other_guests[:len(other_guests) - 2]
            

        content = '<p>' + desc + '</p><p class="date no-wrap">' + episode['date'] + '</p><p><a href="https://www.bbc.co.uk/sounds/play/' + episode['episode_link'].split('/').pop() + '" target="_blank">listen &nearr;</a></p><p>' + guest + ' is the ' + prev_guest_title + '<br/>Also featuring: ' + other_guests + '</p>'
        meta_content = ranking_placeholder

        guest_html += '<li><div><h3>' + episode['topic'] + '</h3></div><div class="episode-content"><div class="content-col">' + content + '</div><div class="wiki-col">' + wiki_link + '</div><div class="meta-col">' + meta_content + '</div></div></li>'
    guest_html += '</ol>'
    
    w = open('./../guests/' + guest.replace(' ', '_') + '.html', 'w')
    w.write('<!DOCTYPE html><html lang="en"><head><meta http-equiv="Content-Type"content="text/html; charset=UTF-8" /><link rel="stylesheet" type="text/css" href="./../client/css/common.01.css" /><link rel="stylesheet" type="text/css" href="./../client/css/guest.01.css" /><script src="./../client/util.js"></script><script src="./../client/guest-page.js"></script><meta http-equiv="X-UA-Compatible" content="IE=edge" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="robots" content="index,follow" /><meta name="googlebot" content="index,follow" /><meta property="og:title" content="' + guest +'" /><meta property="og:description" content="" /><meta name="theme-color" content="#000"><title>' + guest + '</title><link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Official_portrait_of_Lord_Bragg_crop_2.jpg/440px-Official_portrait_of_Lord_Bragg_crop_2.jpg" /></head><body><main>' + guest_html + '</main></body></html>')
    w.close()

def sortByCount(name):
    return frequency[name]['count']

# begin all guests page
index_html = '<header><p class="header-back-link"><a href="./../">&larr; episodes</a></p><h1>All guests</h1></header>'
index_html += '<ul>'
for guest in sorted(sorted(frequency.keys()), key=sortByCount, reverse=True):
    index_html += '<li>'
    index_html += '<div class="flex-row space-between">'
    index_html += '<div><a href="./../guests/' + guest.replace(' ', '_') + '.html">' + guest + '</a><div><em>' + frequency[guest]['title'][0] + '</em></div></div><div class="text-right"><div class="no-wrap">' + frequency[guest]['last'] + '</div>' 
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

w = open('./../guests/index.html', 'w')
w.write('<!DOCTYPE html><html lang="en"><head><meta http-equiv="Content-Type"content="text/html; charset=UTF-8" /><link rel="stylesheet" type="text/css" href="./../client/css/common.01.css" /><link rel="stylesheet" type="text/css" href="./../client/css/guests.01.css" /><script src="./../client/util.js"></script><script src="./../client/guest-page.js"></script><meta http-equiv="X-UA-Compatible" content="IE=edge" /><meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="robots" content="index,follow" /><meta name="googlebot" content="index,follow" /><meta property="og:title" content="all guests" /><meta property="og:description" content="" /><meta name="theme-color" content="#000"><title>all guests</title><link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Official_portrait_of_Lord_Bragg_crop_2.jpg/440px-Official_portrait_of_Lord_Bragg_crop_2.jpg" /></head><body><main>' + index_html + '</main></body></html>')
w.close()