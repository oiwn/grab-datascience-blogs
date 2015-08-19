import sys
import logging

import feedparser
from grab.spider import Task
from grab.error import DataNotFound
from weblib.etree import get_node_text
# from weblib.feed import parse_feed
from weblib.text import remove_bom
from weblib.error import ResponseNotValid

from .base import BaseSpider
from utils.decorators import validate_page


logger = logging.getLogger('blogs.spider')


class DataScienceBlogsSpider(BaseSpider):
    """ Scrape data science blog from the curated list
    https://github.com/rushter/data-science-blogs

    """
    def page_validator(self, grab):
        # naive check if document is valid html
        try:
            grab.doc('//body').node()
        except DataNotFound:
            raise ResponseNotValid

        if not grab.doc('//title').exists():
            logger.error(
                "Document is not valid: {}".format(grab.response.url))
            raise ResponseNotValid

    def task_generator(self):
        """ Here we go.
        """
        # blogs = list(self.parse_blogs_list())[:3]
        blogs = self.parse_blogs_list()
        for blog in blogs:
            yield Task('html', url=blog['html'], blog=blog)

        # invalid html document to demonstrate how decorator
        # 'page_validator' work
        yield Task('html', url="https://api.github.com")

    @validate_page('page_validator')
    def task_html(self, grab, task):
        """ Process index page for each blog to extract
        valuable data

        """
        logger.info("Get blog: {}".format(grab.response.url))
        # find nodes with text
        nodes_with_text = filter(
            None,
            map(
                lambda x: x.strip(),
                grab.doc('//body//*').text_list()
            )
        )

        # extract text from the document
        # excluding script and style tags
        doc_text = get_node_text(
            grab.doc('//body').node(),
            smart=True
        ).encode('utf-8', 'ignore')

        page_params = {
            'doc_size_bytes': sys.getsizeof(grab.response.body),
            'doc_size_chars': len(grab.response.body),
            'nodes_with_text': len(nodes_with_text),
            'content_text_chars': len(doc_text),
            'content_text_bytes': sys.getsizeof(doc_text),
        }

        # extract links to scripts and css
        # used on page
        scripts = grab.doc(
            '//script[@src]').attr_list('src')
        css = grab.doc(
            '//link[@rel="stylesheet"]').attr_list('href')

        page_imports = {
            'scripts': filter(None, scripts),
            'css': filter(None, css),
        }

        # extract meta attributes
        page_meta = {
            'title': grab.doc('//title').text().lower(),
            'description': grab.doc(
                '//meta[contains(@name, "description")]'
            ).attr('content', default=u"").lower(),
            'keywords': grab.doc(
                '//meta[contains(@name, "keywords")]'
            ).attr('content', default=u"").lower(),
            'charset': grab.doc('//meta[@charset]').attr(
                'charset', default=u"").lower()
        }

        data = {
            'blog': task.blog,
            'source_url': grab.response.url,
            'params': page_params,
            'imports': page_imports,
            'meta': page_meta,
        }
        self.save_blog(data)

        # get rss feed for this blog
        # we clone grab object so it would be
        # if user go to the blog page and click rss link
        g = grab.clone()
        g.setup(url=task.blog['rss'])
        yield Task('rss', grab=g, data=data)

    def task_rss(self, grab, task):
        """ Extract some information from rss feed
        """
        logger.info("Get rss: {}".format(grab.response.url))

        all_authors = set()
        all_tags = set()
        all_titles = []

        feed = feedparser.parse(remove_bom(grab.response.body))

        # feed = parse_feed(grab)['feed']

        feed_entries = len(feed['entries'])
        # if feed_entries > 0:
        #     print feed['entries'][0].keys()

        for entry in feed['entries']:
            if 'author' in entry:
                all_authors.add(entry['author'].lower())
            if 'tags' in entry:
                tags = filter(None, map(
                    lambda x: x['term'].lower(),
                    entry['tags']
                ))
                all_tags |= set(tags)  # union operator
            if 'title' in entry:
                all_titles.append(entry['title'].lower())

        if 'bozo_exception' in feed:
            logger.error(
                "Error parsing feed: {}".format(feed['bozo_exception']))

        feed_parsing_error = (str(feed['bozo_exception'])
                              if 'bozo_exception' in feed else '')
        content = {
            'authors': list(all_authors),
            'tags': list(all_tags),
            'titles': list(all_titles),
            'entries': feed_entries,
            'error': feed_parsing_error,
        }

        # we put this data into the task object in previous handler
        data = task.data
        data['content'] = content
        self.save_blog(data)
