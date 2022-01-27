import scrapy
from scrapy import Request
from ..items import ArticleItem

class F1Spider(scrapy.Spider):
    name = "sprint"
    allowed_domains = ["www.formula1.com"]
    start_urls = ['https://www.formula1.com/en/results.html/2021/races.html']

    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[0].css(".resultsarchive-filter-item")[1].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[0].css(".resultsarchive-filter-item")[1].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_gp)

    def parse_gp(self, response):
        title = response.css('title::text').extract_first()
        li = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
        for num in li:
            if num == 10 or num == 14 or num == 19:
                all_links = {
                    name:response.urljoin(url) for name, url in zip(
                    response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[num].css("span::text").extract(),
                    response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[num].css("a::attr(href)").extract())
                }
                for link in all_links.values():
                    yield Request(link, callback=self.parse_sprint)
            else:
                continue
                #yield {
                #    "title":title,
                #    "all_links":all_links
                #}
        

    def parse_sprint(self, response):
        #title = response.css(".resultsarchive-side-nav").css(".side-nav-item")[3].css("a::text").extract()


        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-side-nav").css(".side-nav-item")[5].css("a::text").extract(),
            response.css(".resultsarchive-side-nav").css(".side-nav-item")[5].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_category)

    def parse_qualif_spa(self, response):
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
            Position = article.css(".dark").css("td::text").extract_first()
            Number = article.css(".dark.hide-for-mobile").css("td::text").extract_first()
            Driver = article.css(".hide-for-mobile").css("span::text").extract_first()
            Team = article.css(".semi-bold.uppercase.hide-for-tablet").css("td::text").extract_first()
            Points = article.css(".bold")[3].css("td::text").extract_first()
            yield ArticleItem(
                title = title,
                Date = Date,
                Position = Position,
                Number = Number,
                Driver = Driver,
                Team = Team,
                Points = Points

            )

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())

"""  
yield {
            "title":title,
            "all_links":all_links
        }"""