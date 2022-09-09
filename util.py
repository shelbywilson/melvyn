def parse_page(url, link):
    html_page_follow = urllib.request.urlopen(url)
    html_page_follow_soup = BeautifulSoup(html_page_follow, "html.parser")

    author = html_page_follow_soup.find(id="bio").find('h2').get_text().strip()
    vocation = html_page_follow_soup.find(id="bio").select('.vocation')[0].get_text().strip()
    date = link.select('.date')[0].get_text().strip()
    title = html_page_follow_soup.find('h1').get_text().strip().replace('"', '\"')
    subtitle = ''
    if (html_page_follow_soup.select('#content')[0].find('em')): 
        subtitle = html_page_follow_soup.select('#content')[0].find('em').get_text().strip()

    recommendations = get_recs(html_page_follow_soup, author)

    print('\n' + url)
    print(author + ' ' + str(len(recommendations)))

    return {'author': author, 'url': url, 'vocation': vocation, 'date': date, 'title': title, 'subtitle': subtitle, 'recommendations': recommendations}