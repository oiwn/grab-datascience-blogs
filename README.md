# Scrape data science blogs data using Grab framework.

Yo dawg! I heard that you like X, so we put Y in your X so you can Y while you Z.

# What is it?

Grab is one of the best web scraping framework for practical purposes but unfortunately
it was never introduced for the worldwide community. Lorien finished English documentation
yearly this year so i think it's a right time time to break the wall.

### Description

There is data science blogs list by Rushter - https://github.com/rushter/data-science-blogs
And web scraping framework named Grab by Lorien - https://github.com/lorien/grab

The main idea is to use Grab to collect data about data science blog from Rushter collection.

# Install

I suggest you to create separate project environment.

```
mkvirtualenv grabdatascience
workon grabdatascience
```

Clone project and install required dependencies..

```
git clone https://github.com/istinspring/grab-datascience-blogs.git
cd grab-datascience-blogs
pip install -r requirements.txt
```

# Prepare

First of all you need to download blogs list into the project's ```var/``` directory.

```
wget https://raw.githubusercontent.com/rushter/data-science-blogs/master/data-science.opml -P var/
```

# Results

I added few find/aggregation requests to extract interesting data from mongo.
Use ```python cli.py --stats``` to print it.

```
Blogs in database: 98

Top 10 tags:
        machine learning - 26
        data science - 25
        python - 23
        r - 14
        uncategorized - 14
        data - 12
        deep learning - 11
        big data - 10
        visualization - 8
        data mining - 7

Authors with post in more than one blog:
david taylor (noreply@blogger.com) - 2
[u'http://www.prooffreader.com/', u'http://prooffreaderplus.blogspot.ca/']
ryan swanstrom - 2
[u'http://101.datascience.community/', u'http://blog.sense.io/']

16 blogs based on twitter bootstrap css.
42 blogs on wordpress CMS.
6 blogs on Octopress.
```
