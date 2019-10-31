import scrapy
from crawler.items import desmogOrgan
import re
import json
import os




profile_json = open("C:\Project\citationNetwork\crawler\crawler\profiles.json", "r")
profiles = json.load(profile_json)


class desmogSpide(scrapy.Spider):
    name = "desmog"


    def start_requests(self):
        urls = []
        path = os.getcwd()
        cache = "http://webcache.googleusercontent.com/search?q=cache:"
        with open("crawler/test.txt", "r") as file:
            for line in file:
                urls.append(line.strip())

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        # get name of organization
        organization_name = response.css("title::text").get().split(" | ")[0]

        # list of key people
        key_people_list = list()

        # list of related organization
        related_org_list = list()


        # get raw contents of key people from the datasets
        # Place 1 to get name
        key_people_raws = response.xpath("//h2[contains(text(), 'People')]/following::li/strong[preceding::h2[1][contains(text(), 'People')]]")
        for each_raw in key_people_raws:
            name = re.sub(r'<.*?>', '', each_raw.get())
            name = name.replace("\xa0", " ").strip()
            key_people_list.append(name)


        # place 2 to get name
        key_people_tables = response.xpath("//h2[contains(text(), 'People')]/following::tbody[preceding::h2[1][contains(text(), 'People')]]")
        for table in key_people_tables:
            name_lists = table.css("tr")
            for i in range(1, len(name_lists)):
                name = name_lists[i].css("td")[0]
                name = re.sub(r'<.*?>', '', name.get())
                name = name.replace("\xa0", " ").strip()

                key_people_list.append(name)

        # get raw contents of related organizations from the datasets
        related_org_raws = response.xpath("//h2[contains(text(), 'Related')]/following::strong[preceding::h2[1][contains(text(), 'Related')]]")
        for each_raw in related_org_raws:
            # get clean organization name
            name = re.sub(r'<.*?>', '', each_raw.get())
            name = name.replace("\xa0", " ").strip()
            related_org_list.append(name)

        organization_url = response.url.replace("http://webcache.googleusercontent.com/search?q=cache:", "")

        yield desmogOrgan(name=organization_name, url=organization_url, related_organs=related_org_list, key_people=key_people_list)


#



