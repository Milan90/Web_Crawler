from requests_html import HTMLSession


def find_links(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    links = r.html.absolute_links
    title = r.html.find('title', first=True).text

    return {'title': title,
            'links': links}


def side_map(url):
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
