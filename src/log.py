import logging

log = logging.getLogger('conferences')

log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)
