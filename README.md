# WebCrawler
Getting started:
- Edit config
- pip install -r requirement.txt
- python3 main.py

Known flaws:
- Use asynchronous io
- Use os independant file seperators
- Identify and avoid duplicate HTML elements within different pages
- Handle 'honey pots' of urls
- Explore DFS instead of BFS
- Testing of link_finder and 

Favourite features:
- Multithreading for faster performance
- Scrapes all static assets, including files held on the domain
- Prevents duplicating work by holding visited urls and files in a set
- Simple API for instantiating Crawler
