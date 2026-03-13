import sys, requests
from bs4 import BeautifulSoup


def get_page_content():
    base_url = "https://en.wikipedia.org"
    headers = {
        "User-Agent": "PiscineDjango (42mulhouse)"
    }
    res = requests.get(base_url + globals()["next_search"], headers=headers)
    if not res.status_code == 200:
        print(f"Search failed for {base_url + globals()["next_search"]} : {res}")
        return
    print(base_url + globals()["next_search"])
    return BeautifulSoup(res.content, features="html.parser")

def get_first_link(soup):
    for p in soup.select_one("div.mw-content-ltr.mw-parser-output").find_all("p", recursive=False):
        for link in p.find_all("a", href=True, recursive=False):
            if (link["href"].startswith("/wiki/") and
                not link["href"].startswith("/wiki/Help:") and 
                link["href"] != globals()["next_search"]) :
                return link["href"]

    # second try without recursive, some pages are weird
    for p in soup.select_one("div.mw-content-ltr.mw-parser-output").find_all("p"):
        for link in p.find_all("a", href=True, recursive=False):
            if (link["href"].startswith("/wiki/") and 
                not link["href"].startswith("/wiki/Help:") and 
                link["href"] != globals()["next_search"]):
                return link["href"]

    # third try to may refer to pages
    for link in soup.select_one("div.mw-content-ltr.mw-parser-output").find_all("a", href=True):
        if (link["href"].startswith("/wiki/") and 
            not link["href"].startswith("/wiki/Help:") and 
            not link["href"].startswith("/wiki/File:") and 
            link["href"] != globals()["next_search"]):
            return link["href"]
    return None

def add_page_to_path(soup):
    page_title = soup.select_one(".mw-page-title-main")
    if not page_title:
        print("Error while parsing page title")
    globals()["path"].append(page_title.contents[0])

def is_philosophy():
    return globals()["path"][-1] == "Philosophy"

def is_looping():
    current = globals()["path"][-1]
    for p in globals()["path"][:-1]:
        if p == current:
            return True
    return False

def explore_wikipedia():
    soup = get_page_content()
    if not soup:
        return False
    add_page_to_path(soup)

    if is_philosophy():
        for link in globals()["path"]:
            print(link)
        print(f"{len(globals()["path"])} roads from {sys.argv[1]} to philosophy")
        return False

    if is_looping():
        print("It leads to an infinite loop !")
        return False

    first_link = get_first_link(soup)
    if not first_link:
        print("It leads to a dead end !")
        return False

    globals()["next_search"] = first_link
    return True

def roads_to_philosophy():
    if len(sys.argv) != 2:
        print("You must provide only your search term")
        return

    globals()["path"] = []
    globals()["next_search"] = f"/wiki/{sys.argv[1].replace(' ', '_')}"

    while explore_wikipedia():
        pass

if __name__ == "__main__":
    roads_to_philosophy()