import scrapy
from scrapy import Request
from ..items import ArticleItem

class F1Spider(scrapy.Spider):
    name = "f1_parse"
    allowed_domains = ["www.formula1.com"]
    start_urls = ['https://www.formula1.com/en/results.html/2021/races.html']

    def parse(self, response):
        #title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[1:].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[1:].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_category)
       
    def parse_category(self, response):
        title = title = self.clean_spaces(response.css(".ResultsArchiveTitle").css("h1::text").extract_first())
        for article in response.css(".resultsarchive-table").css("tbody"):
            Position = article.css(".dark").css("td::text")[0].extract()
            Number = article.css(".dark.hide-for-mobile").css("td::text").extract()
            Driver = article.css(".hide-for-mobile").css("span::text").extract()
            Team = article.css(".semi-bold.uppercase.hide-for-tablet").css("td::text").extract()
            Laps = article.css(".bold.hide-for-mobile")[1].css("td::text").extract()
            Time = article.css(".dark.bold")[1].css("td::text").extract()
            Points = article.css(".bold")[3].css("td::text").extract()
            yield ArticleItem(
                title = title,
                Position = Position,
                Number = Number,
                Driver = Driver,
                Team = Team,
                Laps = Laps,
                Time = Time,
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