# -*- coding: utf-8 -*-
import scrapy

from hkwanted.items import wantedPerson

class HkwantedspiderSpider(scrapy.Spider):
    name = "hkwantedspider"
    start_urls = [
        "http://www.icac.org.hk/en/law_enforcement/wp/index_name.html"
    ]

    def parse(self, response):
        links = response.css(".photoFrame::attr(href)").extract()
        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        person = wantedPerson()
        person['photolink'] = response.urljoin(response.css("img:nth-child(4)::attr(src)").extract_first())

        namecharges = response.css("table")[1].css("td::text").extract()
        person['name'] = namecharges[0].split(" : ")[1]
        charges = namecharges[1:]; charges[0] = charges[0].split(" : ")[1]; charges = map(lambda x: x.strip(",\t\r\n\s"), charges)
        person['charges'] = charges

        badstuff = response.css(".tb_line").css("td::text").extract()
        person['casebrief'] = badstuff[-1]
        particulars = map(lambda x: x.replace("\t",""), badstuff[:-1])
        particulars = map(lambda x: x.replace(";",""), re.findall(r"(?=;([^;]*?:.*?);[^;:]*:)", ";"+";".join(badstuff[:-1])))
        particulars = map(lambda x: x.split(":"), particulars)
        person['particulars'] = {d[0].strip():d[1].strip() for d in particulars}

        yield person
