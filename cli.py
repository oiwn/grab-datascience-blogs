import re
import logging
import argparse

from weblib.logs import default_logging

from spiders.blogs import DataScienceBlogsSpider
from settings import db_connection


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    default_logging(grab_log='var/grab.log', level=logging.DEBUG, mode='w',
                    propagate_network_logger=False,
                    network_log='var/grab.network.log')

    parser = argparse.ArgumentParser(description='command line interface')
    parser.add_argument(
        '-S', '--scrape-blogs', type=str,
        help='scrape blogs from provided *.opml file')
    parser.add_argument(
        '--stats', action="store_true", default=False,
        help='print some stats'
    )

    args = parser.parse_args()

    if args.scrape_blogs:
        spider = DataScienceBlogsSpider.get_instance(
            data_science_blogs_list=args.scrape_blogs)
        spider.run()
        # logger.info(spider.render_stats())
    elif args.stats:
        db = db_connection()
        print("Blogs in database: {}".format(
            db['blogs'].count()
        ))

        # calculate top 10 tags
        print("Top 10 tags:")
        pipeline = [
            {"$match": {"content.tags": {"$not": {"$size": 0}}}},
            {"$project": {"content.tags": 1}},
            {"$unwind": "$content.tags"},
            {"$group": {"_id": "$content.tags", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        results = db.command("aggregate", "blogs", pipeline=pipeline)
        for res in results['result']:
            print("\t" + res['_id'] + " - " + str(res['count']))
        print

        print("Authors with post in more than one blog:")
        pipeline = [
            {"$match": {"content.authors": {"$not": {"$size": 0}}}},
            {"$project": {"content.authors": 1, "source_url": 1}},
            {"$unwind": "$content.authors"},
            {
                "$group": {
                    "_id": "$content.authors",
                    "count": {"$sum": 1},
                    "blogs": {"$addToSet": "$source_url"}
                }
            },
            {"$match": {"count": {"$gt": 1}}},
        ]

        results = db.command("aggregate", "blogs", pipeline=pipeline)
        for res in results['result']:
            print(
                "\t" + res['_id'] + " - " + str(res['count']) +
                " - " + str(res['blogs']))
        print

        # blogs based on twitter bootstrap
        # db.blogs.find({ "imports.css": {$in: [/bootstrap/]} }).count();
        results = db['blogs'].find(
            {
                "imports.css": {
                    "$in": [re.compile(r'bootstrap')],
                },

            },
            {
                "source_url": True,
            }
        )
        print(
            "{} blogs based on twitter bootstrap css.".format(
                results.count())
        )
        # print ", ".join(map(lambda x: x['source_url'], results))

        results = db['blogs'].find(
            {
                "imports.css": {
                    "$in": [re.compile(r'wp-content')],
                },

            },
            {
                "source_url": True,
            }
        )
        print(
            "{} blogs on wordpress CMS.".format(
                results.count())
        )

        results = db['blogs'].find(
            {
                "imports.scripts": {
                    "$in": [re.compile(r'octopress')],
                },

            },
            {
                "source_url": True,
            }
        )
        print(
            "{} blogs on Octopress.".format(
                results.count())
        )

    else:
        parser.print_help()
