from .req import get

class rule34():
    def search(tags, limit=None):
        return get(tags, limit)
    def get_random_post(limit=None):
        return get(None, limit)
    