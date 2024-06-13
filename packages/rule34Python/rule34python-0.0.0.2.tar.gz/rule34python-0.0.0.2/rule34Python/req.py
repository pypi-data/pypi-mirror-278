import requests
from xml.etree import ElementTree

def get(param, limit=None):
    try:
        if limit:
            r = requests.get(f"https://api.rule34.xxx//index.php?page=dapi&s=post&q=index&tags={param}&limit={limit}")
        else:
            r = requests.get(f"https://api.rule34.xxx//index.php?page=dapi&s=post&q=index&tags={param}")
    except Exception as e:
        raise Exception(f"ERROR: > {e}\n\n\nPlease Contact evergaster or Open a Issue in https://github.com/EverGasterXd/sara_api/issues")
    else:
        try:
            tree = ElementTree.fromstring(r.content)
            file_urls = [post.attrib['file_url'] for post in tree.findall('post')]
            return file_urls[:limit] if file_urls else None
        except Exception as e:
            raise Exception(f"ERROR: > {e}\n\n\nPlease Contact evergaster or Open a Issue in https://github.com/EverGasterXd/sara_api/issues")