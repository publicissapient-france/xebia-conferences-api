from utils import pretty_dumps
import os
from datetime import datetime
from eventbrite import Eventbrite

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
        self._slug = conf_slug

        log.debug("Initializing conference object for {conf_id}"
                  " from dict: {source_dict}".format(
                    conf_id=self.id,
                    source_dict=pretty_dumps(source_dict)))

        if 'date' in source_dict and 'dates' in source_dict:
            raise ConflictingFieldsException

        self.title = source_dict['title']
        self.dates = [datetime.strptime(date, "%Y/%m/%d") for date in source_dict['dates']]
        self.website = source_dict['website']
        self.eventbrite_id = source_dict['eventbrite_id']
        self.has_internal_cfp = 'cfp' in source_dict and 'internal' in source_dict['cfp']
        self.expected_public = source_dict['public']['expected']
        self.location = Location(source_dict['location'])
        self.organizers = source_dict['organizers']
        self.capacity = None
        self.logo = None
        self.status = None
        self.venue = None
        self.fetch_eventbrite()

    def json(self):
        return {
            "title": self.title,
            "meta_year": self.meta_year,
            "meta_slug": self._slug,
            "dates": [date.strftime("%Y/%m/%d") for date in self.dates],
            "website": self.website,
            "has_internal_cfp": self.has_internal_cfp,
            "expected_public": self.expected_public,
            "location": self.location.name,
            "address": self.location.address,
            "organizers": self.organizers,
            "capacity": self.capacity,
            "logo": self.logo,
            "status": self.status,
            "venue": self.venue
        }

    def pretty(self):
        items = [
            "====== " + self.title + " ======",
            "ID: " + self.meta_year + "/" + self._slug,
            "Dates: " + "".join(["\n  - " + date.strftime("%Y/%m/%d")
                                 for date in self.dates]),
            "Website: " + self.website,
            "Location: " + self.location.name,
            "Address: " + self.location.address,
            "Expected public: " + self.expected_public,
            "Has an internal CFP: " + str(self.has_internal_cfp),
            "Venue: " + pretty_dumps(self.venue)
        ]
        return '\n'.join(items) + '\n'

    def fetch_eventbrite(self):
        try:
            if not self.eventbrite_id or "?" in self.eventbrite_id:
                raise Exception("No valid Eventbrite ID founnd")
            eventbrite = Eventbrite(os.environ['EVENTBRITE_TOKEN'])
            event = eventbrite.get_event(self.eventbrite_id)
            log.error(pretty_dumps(event))
        except Exception as e:
            log.error(e)
            self.capacity = self.expected_public
            self.logo = "http://www.technobuffalo.com/wp-content/uploads/2014/09/DuckDuckGo-Logo.jpg"
            self.status = "unknown"
            self.venue = "unknown"
            return
        self.capacity = event["capacity"]
        self.logo = event["logo"]
        self.status = event["status"]
        self.venue = eventbrite.get_venue(event["venue_id"])
