import requests, json, sys

def get_references(name):
    headers = {
        "User-Agent": "PiscineDjango (42mulhouse)"
    }
    params = {
        "action": "query",
        "prop": "extlinks",
        "format": "json",
        "titles": name,
        "ellimit": 500
    }

    references_request = requests.api.get("https://en.wikipedia.org/w/api.php", headers=headers, params=params)
    if not references_request.ok:
        print(f"Request failed : {references_request.reason}")
        return 

    references_data = references_request.json()
    if "error" in references_data:
        print(f"Server returned error : {references_data['error']['info']}")
        return
    
    references_pages = references_data["query"]["pages"]
    references = next(iter(references_pages.items()))[1]
    if not "extlinks" in references:
        return 
    return (references["extlinks"])

def get_categories(name):
    headers = {
        "User-Agent": "PiscineDjango (42mulhouse)"
    }
    params = {
        "action": "query",
        "prop": "categories",
        "format": "json",
        "titles": name,
    }

    category_request = requests.api.get("https://en.wikipedia.org/w/api.php", headers=headers, params=params)
    if not category_request.ok:
        print(f"Request failed : {category_request.reason}")
        return 

    category_data = category_request.json()
    if "error" in category_data:
        print(f"Server returned error : {category_data['error']['info']}")
        return

    category_pages = category_data["query"]["pages"]
    categories = next(iter(category_pages.items()))[1]
    if not "categories" in categories:
        return 
    return (categories["categories"])

def get_extract(name):
    headers = {
        "User-Agent": "PiscineDjango (42mulhouse)"
    }
    params = {
        "action": "query",
        "prop": "extracts",
        "format": "json",
        "titles": name,
        "explaintext": True,
        "exsectionformat": "plain",
        "exintro": True,
        "exlimit": 1
    }

    extract_request = requests.api.get("https://en.wikipedia.org/w/api.php", headers=headers, params=params)
    if not extract_request.ok:
        print(f"Request failed : {extract_request.reason}")
        return 

    extract_data = extract_request.json()
    if "error" in extract_data:
        print(f"Server returned error : {extract_data['error']['info']}")
        return

    extract_pages = extract_data["query"]["pages"]
    page_data = next(iter(extract_pages.items()))[1]
    if len(page_data["extract"]) == 0:
        return 
    return (page_data)

def get_search_results():
    headers = {
        "User-Agent": "PiscineDjango (42mulhouse)"
    }
    params = {
        "action": "opensearch",
        "format": "json",
        "search": sys.argv[1],
        "limit": 5
    }

    search_request = requests.api.get("https://en.wikipedia.org/w/api.php", headers=headers, params=params)
    if not search_request.ok:
        print(f"Request failed : {search_request.reason}")
        return 

    search_data = search_request.json()
    if "error" in search_data:
        print(f"Server returned error : {search_data['error']['info']}")
        return

    return (search_data)


def search_wikipedia():

    if len(sys.argv) != 2:
        print("Wrong input, expecting only search term")
        return

    file = ""
    search_data = get_search_results()
    for e in search_data[1]:
        extract = get_extract(e)
        categories = get_categories(e)
        references = get_references(e)
        if not extract:
            continue
        file += "* " + extract["title"] + "\n\n"
        file += extract["extract"] + "\n\n"
        file += "** " + "References : " + "\n"
        for ref in references:
            file += "\t" + ref["*"] + "\n"
        file += "\n"
        file +=  "** " + "Categories : " + "\n"
        for cat in categories:
            file += "\t" + cat["title"].replace("Category:", "") + "\n"
        file += "\n\n"
    
    if len(file) == 0:
        print(f"Nothing was found about {sys.argv[1]}")
        return

    with open(sys.argv[1].replace(" ", "_").replace("\t", "_").replace("\n", "_") + ".wiki", "w") as f:
        f.write(file)

if __name__ == "__main__":
    search_wikipedia()
