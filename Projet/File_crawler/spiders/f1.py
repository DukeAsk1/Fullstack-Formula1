import scrapy
from scrapy import Request
from ..items import ArticleItem



class F1Spider(scrapy.Spider):
    name = "f1"
    allowed_domains = ["www.formula1.com/en/results.html/2021/races.html"]
    start_urls = ['https://www.formula1.com/en/results.html/2021/races.html']

    def parse(self, response):
        #title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[1].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[1].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_category)

    def parse_category(self, response):
        #for infos in response.css(".date")[0]:
        #    Grand_Prix = infos.css("span::text").extract()
        for article in response.css(".resultsarchive-table")[0]:
            Position = self.clean_spaces(article.css(".dark").css("td::text").extract_first())
            Number = article.css(".dark.hide-for-mobile").css("td::text").extract_first()
            Grand_Prix = self.clean_spaces(article.css(".dark.bold.ArchiveLink").css("a::text").extract_first())
            Date = article.css(".dark.hide-for-mobile").css("td::text").extract_first()
            First_name = article.css(".dark.bold").css(".hide-for-tablet").css("span::text").extract_first()
            Last_name = article.css(".dark.bold").css(".hide-for-mobile").css("span::text").extract_first()
            Car = article.css(".semi-bold.uppercase.hide-for-tabler").css("td::text").extract_first()
            LAPS = article.css(".bold.hide-for-mobile").css("td::text").extract_first()
            Time = article.css(".dark.bold").css("td::text").extract_first()
            Points = article.css(".bold").css("td::text").extract_first()
            yield ArticleItem(
                Position = Position,
                Number = Number,
                #Grand_Prix=Grand_Prix,
                Date=Date,
                First_name = First_name,
                Last_name = Last_name,
                Car = Car,
                Laps = LAPS,
                Time = Time,
                Points = Points
            )

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())