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

I would like to create separated project environment.

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

First of all you need to download blogs list into the project's var/ directory.

```
wget https://raw.githubusercontent.com/rushter/data-science-blogs/master/data-science.opml
```
