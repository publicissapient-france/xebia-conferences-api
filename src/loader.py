import os
import re
import yaml

from log import log
# from utils import pretty_dumps
from conference import Conference


def parse_conferences_from_directory(conferences_directory):
    log.info("Loading conferences from " + conferences_directory)
    conferences = {}
    if not os.path.isdir(conferences_directory):
        log.error("Could not find " + conferences_directory)
        return None
    for base_directory_name, directory_names, file_names in os.walk(conferences_directory):
        for filename in file_names:

            # Ensure that the directory is a year directory
            if not re.match(conferences_directory + "/[0-9]{4}", base_directory_name):
                log.warning("Found {directory} that does not match expected "
                            "directory format".format(directory=base_directory_name))
            conf_year = base_directory_name[-4:]  # TODO use re groups instead

            # Ensure that the filename is valid
            if not re.match("[a-z]+.yml", filename):
                log.warning("Found {filename} that does not match expected "
                            "file format".format(filename=filename))
            conf_slug = filename[:-4]  # TODO use re groups instead

            conf_id = conf_year + '/' + conf_slug
            log.debug("Found conference {conf_id}".format(conf_id=conf_id))

            # Load YAML
            with open(os.path.join(base_directory_name, filename), 'r') as f:
                log.info("Loading {file_name}".format(file_name=f.name))
                conf_data = yaml.load(f)
                # if not isinstance(conf_data, dict):
                #     log.error("{file_name} didn't produce a dict when loaded".format(
                #               file_name=f.name))
                #     pass
            try:
                conferences[conf_id] = Conference(conf_id, conf_data,
                                                  conf_year, conf_slug)
            except Exception as e:
                log.error("Failed to initialize Conference: " + str(e))
            # conferences[conf_id] = conf_data
            # conferences[conf_id]['meta_year'] = conf_year
            # conferences[conf_id]['meta_name'] = conf_name
            log.info("Loaded conference {conf_id}".format(conf_id=conf_id))
    return conferences
