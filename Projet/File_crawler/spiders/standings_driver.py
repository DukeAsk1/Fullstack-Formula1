import scrapy
from scrapy import Request
from ..items import ArticleItem

class F1Spider(scrapy.Spider):
    name = "standings_driver"
    allowed_domains = ["www.formula1.com"]
    start_urls = ['https://www.formula1.com/en/results.html/2021/races.html']


    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[0].css(".resultsarchive-filter-item")[1:11].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[0].css(".resultsarchive-filter-item")[1:11].css("a::attr(href)").extract())
        }

        for link in all_links.values():
            yield Request(link, callback=self.parse_gp)

    def parse_gp(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[1].css(".resultsarchive-filter-item")[1].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[1].css(".resultsarchive-filter-item")[1].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_standings)
       
    def parse_standings(self, response):
        title = self.clean_spaces(response.css(".ResultsArchiveTitle").css("h1::text").extract_first())
        for article in response.css(".resultsarchive-table").css("tbody").css("tr"):
            Position = article.css(".dark")[0].css("td::text").extract_first()
            Driver = article.css(".hide-for-mobile").css("span::text").extract_first()
            Nationality = article.css(".dark.semi-bold.uppercase").css("td::text").extract_first()
            Team = article.css(".grey.semi-bold.uppercase.ArchiveLink").css("a::text").extract_first()
            Points = article.css(".dark.bold").css("td::text").extract_first()
            yield ArticleItem(
                title = title,
                Position = Position,
                Driver = Driver,
                Nationality = Nationality,
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