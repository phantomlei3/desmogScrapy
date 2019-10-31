import scrapy
from crawler.items import Webpage
import re
import json
import sys
import os


profile_json = open("C:\Project\citationNetwork\crawler\crawler\profiles.json", "r")
profiles = json.load(profile_json)


class CitationSpide(scrapy.Spider):
    name = "citations"

    def start_requests(self):
        urls = [
                "https://www.naturalnews.com",
                "http://organicseedsoflife.naturalnews.com/organic-seeds-of-life.html",
                "https://halturnerradioshow.com/index.php/en/news-page/world/nasa-climate-change-and-global-warming-caused-by-changes-in-earth-s-solar-orbit-and-axial-tilt-not-man-made-causes",
                "https://www.naturalnews.com/2019-03-28-not-a-single-democrat-voted-for-the-green-new-deal.html",
                "https://www.bbc.com/news/science-environment-48964736",
                "http://climatesciencenews.com"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # helper function
    # remove social media share links and redundant links
    def remove_share(self, links):
        citations = set()
        for link in links:
            if "facebook?linkurl" in link:
                continue
            if "twitter?linkurl" in link:
                continue
            if "google_plus?linkurl" in link:
                continue
            if "share" in link:
                continue
            # not a format of url
            if "http" not in link:
                continue
            citations.add(link)

        return list(citations)



    def parse(self, response):

        response_profile = None
        # check if the link is in profiles
        for link, profile in profiles.items():
            if link in response.url:
                response_profile = profile
                break

        # if profile exists, extract further citations
        if response_profile is not None:
            title = response.css("title::text").get()
            citation_lists = response.css(response_profile["citations"]).extract()
            # if website does not contain any citations, we assume to move on.
            if len(citation_lists) == 0:
                yield Webpage(title=title, url=response.url)

            else:
                author = response.css(response_profile["author"]).get()
                publish_time = response.css(response_profile["publish_time"]).get()
                # remove social media share links and redundant links
                citation_lists = self.remove_share(citation_lists)

            yield Webpage(title=title, url=response.url, citations=citation_lists, author=author, publish_time=publish_time)
        else:
            # if not in profile, just get a title
            title = response.css("title::text").get()
            yield Webpage(title=title, url=response.url)





