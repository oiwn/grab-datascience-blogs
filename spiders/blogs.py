import sys
import logging
from grab.spider import Task
from weblib.etree import get_node_text
from weblib.feed import parse_feed

from .base import BaseSpider


logger = logging.getLogger('blogs.spider')


class DataScienceBlogsSpider(BaseSpider):
    def task_generator(self):
        for blog in self.parse_blogs_list():
            # yield Task('html', url=blog['html'], blog=blog)
            yield Task('rss', url=blog['rss'], blog=blog)

    def task_html(self, grab, task):
        # naive check if document is html
        if not grab.doc('//body').exists():
            return

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

        # extract links to cripts and css
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
            'title': grab.doc('//title').text(),
            'description': grab.doc(
                '//meta[contains(@name, "description")]'
            ).attr('content', default=u""),
            'keywords': grab.doc(
                '//meta[contains(@name, "keywords")]'
            ).attr('content', default=u""),
            'charset': grab.doc('//meta[@charset]').attr(
                'charset', default=u"")
        }

        page_data = {
            'blog': task.blog,
            'page_url': grab.response.url,
            'params': page_params,
            'imports': page_imports,
            'meta': page_meta,
        }
        print page_data

    def task_rss(self, grab, task):
        print grab.response.url
        print parse_feed(grab)['feed']
