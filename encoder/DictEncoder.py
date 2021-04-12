from json import JSONEncoder


class DictEncoder(JSONEncoder):
    """
    JSON Encoder, that treats every object as a dict
    """
    def default(self, o): return o.__dict__
