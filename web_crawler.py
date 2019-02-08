from requests_html import HTMLSession


def find_links(url):
    """
        This function collects title and all links from given url address.
        It uses Requests-HTML library  which provide lots of powerful tools for scraping the web
        Request-HTML doc: https://html.python-requests.org/
        It will download Chromium into your home directory. This only happens once.

        :param url: url of website from which you want to collect links
        :return: dictionary of keys: title and links
                    {'title': val, 'links': set()}
    """
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    links = r.html.absolute_links
    title = r.html.find('title', first=True).text

    return {'title': title,
            'links': links}


def side_map(url):
    """
        This function rides thru all accessible pages of given domain and collects it creating a map of that domain.
        :param url: url of website which you want to create a map
        :return: dictionary of dictionaries with url address, page title and available links
                example:
                {
                  'http://0.0.0.0:8000': {
                    'title': 'Index',
                    'links': {'http://0.0.0.0:8000/example.html', 'http://0.0.0.0:8000/site.html'}
                }
    """
    map = {url: find_links(url)}
    to_visit = list(map[url]['links'])
    visited = []

    while to_visit:
        for link in to_visit:
            if link not in visited and link.startswith(url):
                visited.append(link)
                to_visit.remove(link)
            else:
                to_visit.remove(link)
                continue
            try:
                new_links = find_links(link)
            except Exception:
                to_visit.remove(link)

            map[link] = new_links
            to_visit.extend(map[link]['links'])

    return map
