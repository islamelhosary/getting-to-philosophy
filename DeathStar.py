import os
import sys
import logging

from wikipedia_jumper import WikipediaJumper


# Initialize Logging ##########################

# We'll just use the root logger for now
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO'))
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    MAX_HOPS = 30
    try:
        MAX_HOPS = int(os.getenv('MAX_HOPS', 30))
    except ValueError:
        logger.error(
            "MAX_HOPS expected to be int found {max_hops}".format(
                max_hops=os.getenv('MAX_HOPS', 30)))

    DELAY_BETWEEN_REQUESTS = 30
    try:
        DELAY_BETWEEN_REQUESTS = int(os.getenv('DELAY_BETWEEN_REQUESTS', 30))
    except ValueError:
        logger.error(
            "DELAY_BETWEEN_REQUESTS expected to be int found {deley}".format(
                max_hops=os.getenv('DELAY_BETWEEN_REQUESTS', 30)))

    jumper = WikipediaJumper(max_hops=MAX_HOPS,
                             DELAY_BETWEEN_REQUESTS=DELAY_BETWEEN_REQUESTS,
                             VERBOSE=True)
    if len(sys.argv) == 1:
        jumper.to_philosophy_and_beyond()
    else:
        jumper.to_philosophy_and_beyond(sys.argv[1])
