import os
import logging
import time
import re
import urllib.parse

import requests
import requests_cache
import lxml.html as lh
from lxml import etree


# Initialize Logging ##########################

# We'll just use the root logger for now
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO'))
)

logger = logging.getLogger(__name__)


class WikipediaJumper(object):
    """Jump between the Wikipedia pages till it reaches Philosophy page"""
    def __init__(self, max_hops, VERBOSE=False, DELAY_BETWEEN_REQUESTS=30):
        self.MAX_HOPS = max_hops
        self.VERBOSE = VERBOSE
        self.BASE_URL = os.getenv('BASE_URL', 'https://en.wikipedia.org/wiki/')
        self.DEFAULT_SEED = os.getenv('DEFAULT_SEED', 'Special:Random')
        self.MAIN_CONTENT_CLASS = os.getenv(
            'MAIN_CONTENT_CLASS', ".mw-parser-output")
        self.CSS_SELECTORS_TO_BE_REMOVED = os.getenv(
            'CSS_SELECTORS_TO_BE_REMOVED',
            '.reference,span,div.hatnote,.thumb,\
            table,a.new,a.external,i,#coordinates,infobox')
        self.all_hops = []
        self.DELAY_BETWEEN_REQUESTS = DELAY_BETWEEN_REQUESTS
        # Initialize the cache
        requests_cache.install_cache(
            'wikipedia-cache',
            backend='sqlite',
            expire_after=(360 * 60 * 60 * 24))

        if self.VERBOSE:
            logger.info(
                "Initialized the jumper with \
                \nMAX_HOPS={MAX_HOPS},\
                \nDELAY_BETWEEN_REQUESTS={DELAY_BETWEEN_REQUESTS},\
                \nDEFAULT_SEED={DEFAULT_SEED},\
                \nMAIN_CONTENT_CLASS={MAIN_CONTENT_CLASS},\
                \nCSS_SELECTORS_TO_BE_REMOVED={CSS_SELECTORS},\
                \nBASE_URL={BASE_URL}\n\n\
                ".format(MAX_HOPS=self.MAX_HOPS,
                         DELAY_BETWEEN_REQUESTS=self.DELAY_BETWEEN_REQUESTS,
                         DEFAULT_SEED=self.DEFAULT_SEED,
                         MAIN_CONTENT_CLASS=self.MAIN_CONTENT_CLASS,
                         CSS_SELECTORS=self.CSS_SELECTORS_TO_BE_REMOVED,
                         BASE_URL=self.BASE_URL,
                         ))

    def next_page_cleaning(self, rel_link):
        # Strip the /wiki/ part to get the page name only.
        rel_link = rel_link[len('/wiki/'):]
        # Unquote the rel_link.
        rel_link = urllib.parse.unquote(rel_link)
        # Remove Anchors from the rel_link.
        idx = rel_link.find('#')
        if idx != -1:
            rel_link = rel_link[:idx]
        return rel_link

    def find_next_page(self, main_content):
        '''Returns next_page from the main content of a page'''
        next_page = None
        # Removes the elements using css classes.
        for elm in main_content.cssselect(self.CSS_SELECTORS_TO_BE_REMOVED):
            elm.drop_tree()
        # Encodes paretheses inside links
        for elm in main_content.cssselect('a'):
            try:
                if 'href' in elm.keys():
                    elm.set('href', urllib.parse.quote(elm.get('href')))
            except TypeError:
                logger.error(
                    "TypeError in {elm_href}".format(elm_href=elm.get('href')))
        # Removes the text inside parentheses
        main_content = lh.fromstring(
            re.sub(r'(\(.*?\))',
                   '',
                   etree.tostring(main_content).decode('utf-8'))
        )
        for elmeent, attribute, link, pos in main_content.iterlinks():
            # Gets only the links with href.
            if attribute != 'href':
                continue
            # Gets only the wiki links.
            if not link.startswith('/wiki/'):
                continue
            # Clean the link.
            next_page = self.next_page_cleaning(link)
            break
        return next_page

    def _jump(self, page):
        '''Returns next_page from the name of a page'''
        if page == self.DEFAULT_SEED:
            with requests_cache.disabled():
                response = requests.get("{0}{1}".format(self.BASE_URL, page))
        else:
            response = requests.get("{0}{1}".format(self.BASE_URL, page))
        # Wait only if there is a cache miss
        IS_CACHED = False
        if 'from_cache' not in response.__dict__.keys():
            time.sleep(self.DELAY_BETWEEN_REQUESTS)
            logger.debug(
                'Cache disabled in Response with keys {r}'.format(
                    r=response.__dict__.keys()))
        elif not response.from_cache:
            time.sleep(self.DELAY_BETWEEN_REQUESTS)
            logger.debug(
                'Cache miss for {res}'.format(res=response.url))
        else:
            IS_CACHED = True
            logger.debug(
                'Cache miss for {res}'.format(res=response.url))

        if self.VERBOSE:
                logger.info("{cached}The Page {init} resolved to {res}".format(
                    cached="__CACHED__:" if IS_CACHED else "",
                    init=page, res=response.url))

        root_tree = lh.fromstring(response.content)
        main_content_list = root_tree.cssselect(self.MAIN_CONTENT_CLASS)
        # Check if the page contains MAIN_CONTENT_CLASS.
        if len(main_content_list) > 0:
            main_content = main_content_list[0]
            return self.find_next_page(main_content)
        else:
            logger.error(
                "Parsing Error: Can't find main_content in Page:{page}".format(
                    page=page))
            return None

    def is_philosophy(self, next_link):
        if next_link == "Philosophy":
            return True
        return False

    def to_philosophy_and_beyond(self, start_url=None):
        self.all_hops = []

        # seed with the default if start_url is null.
        if not start_url:
            start_url = self.DEFAULT_SEED

        next_link = start_url

        # loop till reach philosophy or reach max_hops.
        for i in range(self.MAX_HOPS):
            self.all_hops.append(next_link)

            if self.VERBOSE:
                logger.info("Hop {i} :Surfing {next_link}".format(
                    i=i, next_link=next_link))
            # Make the jump.
            next_link = self._jump(next_link)
            # Detecting no links found or parsing errors.
            if not next_link:
                logger.info(
                    "Entered a blackhole! {current} doesn't have links to surf"
                    .format(current=self.all_hops[-1]))
                break
            # Detecting the loops.
            elif next_link in self.all_hops:
                logger.info(
                    "To Infinity! Infinite Loop detected with {current_page}"
                    .format(current_page=self.all_hops[-1]))
                break
            # Check if philosophy is reached.
            elif self.is_philosophy(next_link):
                logger.info(
                    "Yay\\0/, 42! Reached Philosophy in {hops} hops"
                    .format(hops=len(self.all_hops)))
                break
