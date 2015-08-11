import logging
import argparse

from weblib.logs import default_logging

from spiders.blogs import DataScienceBlogsSpider


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    default_logging(grab_log='var/grab.log', level=logging.DEBUG, mode='w',
                    propagate_network_logger=False,
                    network_log='var/grab.network.log')

    parser = argparse.ArgumentParser(description='command line interface')
    parser.add_argument(
        '-S', '--scrape-blogs', type=str,
        help='scrape blogs from provided *.opml file')
    # parser.add_argument('-c', '--celery',
    #                     action="store_true", default=False,
    #                     help='run as celery task')

    args = parser.parse_args()

    if args.scrape_blogs:
        spider = DataScienceBlogsSpider.get_instance(
            data_science_blogs_list=args.scrape_blogs)
        spider.run()
        logger.info(spider.render_stats())
    else:
        parser.print_help()
