import scrapy
from scrapy import Request
from ..items import ArticleItem

class F1Spider(scrapy.Spider):
    name = "pit_stop"
    allowed_domains = ["www.formula1.com"]
    start_urls = ['https://www.formula1.com/en/results.html/2021/races.html']


    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[0].css(".resultsarchive-filter-item")[1:12].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[0].css(".resultsarchive-filter-item")[1:12].css("a::attr(href)").extract())
        }

        for link in all_links.values():
            yield Request(link, callback=self.parse_gp)

    def parse_gp(self, response):
        #title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[1:].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[1:].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_pitstop)

    def parse_pitstop(self, response):
        #title = response.css(".resultsarchive-side-nav").css(".side-nav-item")[3].css("a::text").extract()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-side-nav").css(".side-nav-item")[3].css("a::text").extract(),
            response.css(".resultsarchive-side-nav").css(".side-nav-item")[3].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_category)
       
    def parse_category(self, response):
        title = self.clean_spaces(response.css(".circuit-info").css("span::text").extract_first())
        Date = self.clean_spaces(response.css(".full-date").css("span::text").extract_first())
        for article in response.css(".resultsarchive-table").css("tbody").css("tr"):
            #Info = article.css("tr").css(" td::text").extract()
            Num_stop = article.css(".dark").css("td::text").extract_first()
            Number = article.css(".dark.hide-for-mobile").css("td::text").extract_first()
            Driver = article.css(".last-name.hide-for-mobile").css("span::text").extract_first()
            Team = article.css(".semi-bold.uppercase.hide-for-tablet").css("td::text").extract_first()
            Laps = article.css(".bold.hide-for-mobile").css("td::text").extract_first()
            Time = article.css(".dark.bold")[2].css("td::text").extract_first()
            yield ArticleItem(
                title = title,
                Date = Date,
                Num_stop = Num_stop,
                Number = Number,
                Driver = Driver,
                Team = Team,
                Laps = Laps,
                Time = Time

            )

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())

"""  
yield {
            "title":title,
            "all_links":all_links
        }"""