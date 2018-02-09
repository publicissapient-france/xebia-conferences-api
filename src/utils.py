import json


class DumbEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return o.json()
        except:
            return o.__str__()


def pretty_dumps(obj):
    """
    Wrapper to json.dumps with convenient parameters
    """
    return json.dumps(obj, indent=4, sort_keys=True, cls=DumbEncoder, ensure_ascii=False)
    # , default=json_serial)
