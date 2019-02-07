from requests_html import HTMLSession


def find_links(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    links = r.html.absolute_links
    title = r.html.find('title', first=True).text

    return {'title': title,
            'links': links}


