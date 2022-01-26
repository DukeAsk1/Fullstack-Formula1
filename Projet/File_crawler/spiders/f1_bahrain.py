import scrapy
from scrapy import Request
from ..items import ArticleItem

class F1Spider(scrapy.Spider):
    name = "f1_bahrain"
    allowed_domains = ["www.formula1.com/en/results.html/2021/races/1064/bahrain/race-result.html"]
    start_urls = ['https://www.formula1.com/en/results.html/2021/races/1064/bahrain/race-result.html']

    def parse(self, response):
        title = self.clean_spaces(response.css(".ResultsArchiveTitle").css("h1::text").extract_first())

        for article in response.css(".resultsarchive-table")[0]:
            Position = article.css(".dark").css("td::text").extract_first()
            Number = article.css(".dark.hide-for-mobile").css("td::text").extract_first()
            Driver = article.css(".dark.bold")[0].css("span::text")[:2].extract()
            Team = article.css(".semi-bold.uppercase.hide-for-tablet").css("td::text").extract_first()
            Laps = article.css(".bold.hide-for-mobile")[1].css("td::text").extract_first()
            Time = article.css(".dark.bold")[1].css("td::text").extract_first()
            Points = article.css(".bold")[3].css("td::text").extract_first()
        
        yield{
            "Title":title,
            "Position":Position,
            "Number":Number,
            "Driver":Driver,
            "Team": Team,
            "Number of Laps": Laps,
            "Time / Retired": Time,
            "Points": Points

        }
        
    

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())

"""for article in response.css("resultsarchive-table")[0]:
            Position = article.css(".dark").css("td::text").extract_first()
            Number = article.css(".dark.hide-for-mobile").css("td::text").extract_first()
            #Date = article.css(".date").css("span::text").extract_first()
            #"""