from utils import pretty_dumps
from datetime import datetime

from log import log
from location import Location


class ConflictingFieldsException(Exception):
    def __int__(self):
        super()


class Conference(object):
    # TODO : Add sponsors handling
    def __init__(self, conf_id, source_dict, conf_year, conf_slug):
        self.id = conf_id
        self.meta_year = conf_year
        self.meta_slug = conf_slug

        log.debug("Initializing conference object for {conf_id}"
                  " from dict: {source_dict}".format(
                    conf_id=self.id,
                    source_dict=pretty_dumps(source_dict)))

        if 'date' in source_dict and 'dates' in source_dict:
            raise ConflictingFieldsException

        self.title = source_dict['title']
        self.dates = [datetime.strptime(date, "%Y/%m/%d") for date in source_dict['dates']]
        self.links = source_dict['links']
        self.website = self.links['website']
        self.has_internal_cfp = 'cfp' in source_dict and 'internal' in source_dict['cfp']
        self.expected_public = source_dict['public']['expected']
        self.location = Location(source_dict['location'])
        self.organizers = source_dict['organizers']

    def json(self):
        return {
            "title": self.title,
            "meta_year": self.meta_year,
            "meta_slug": self.meta_slug,
            "dates": self.dates,
            "links": self.links,
            "website": self.website,
            "has_internal_cfp": self.has_internal_cfp,
            "expected_public": self.expected_public,
            "location": self.location.name,
            "address": self.location.address,
            "organizers": self.organizers
        }

    def pretty(self):
        items = [
            "====== " + self.title + " ======",
            "ID: " + self.meta_year + "/" + self.meta_slug,
            "Dates: " + "".join(["\n  - " + datetime.strftime(date, "%Y/%m/%d")
                                 for date in self.dates]),
            "Website: " + self.website,
            "Location: " + self.location.name,
            "Address: " + self.location.address,
            "Expected public: " + self.expected_public,
            "Has an internal CFP: " + str(self.has_internal_cfp)
        ]
        return '\n'.join(items)
