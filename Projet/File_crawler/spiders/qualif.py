import scrapy
from scrapy import Request
from ..items import ArticleItem

class F1Spider(scrapy.Spider):
    name = "qualif"
    allowed_domains = ["www.formula1.com"]
    start_urls = ['https://www.formula1.com/en/results.html/2021/races.html']

    # def parse():
    #   permet de donner le lien de chaque année étudiée avant 2021  
    #   

    def parse(self, response):
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[0].css(".resultsarchive-filter-item")[2:11].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[0].css(".resultsarchive-filter-item")[2:11].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_gp)
    
    # def parse_gp():
    #   permet de donner le lien de chaque Grand Prix
    #   

    def parse_gp(self, response):
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[1:].css("span::text").extract(),
            response.css(".resultsarchive-filter-container").css(".resultsarchive-filter-wrap")[2].css(".resultsarchive-filter-item")[1:].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_qualif)
    
    # def parse_qualif():
    #   va dans la liste et va chercher l'onglet qualif  

    def parse_qualif(self, response):
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css(".resultsarchive-side-nav").css(".side-nav-item")[5].css("a::text").extract(),
            response.css(".resultsarchive-side-nav").css(".side-nav-item")[5].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_category)

    # def parse_category():
    #   scrappe les informations données par les classes cherchées
    # retourne une liste d'item   
       
    def parse_category(self, response):
        title = self.clean_spaces(response.css(".circuit-info").css("span::text").extract_first())
        Date = self.clean_spaces(response.css(".full-date").css("span::text").extract_first())
        for article in response.css(".resultsarchive-table").css("tbody").css("tr"):
            Position = article.css(".dark").css("td::text").extract_first()
            Number = article.css(".dark.hide-for-mobile").css("td::text").extract_first()
            Driver = article.css(".hide-for-mobile").css("span::text").extract_first()
            Team = article.css(".semi-bold.uppercase.hide-for-tablet").css("td::text").extract_first()
            Q1 = article.css(".dark.bold")[1].css("td::text").extract_first()
            Q2 = article.css(".dark.bold")[2].css("td::text").extract_first()
            Q3 = article.css(".dark.bold")[3].css("td::text").extract_first()
            yield ArticleItem(
                title = title,
                Date = Date,
                Position = Position,
                Number = Number,
                Driver = Driver,
                Team = Team,
                Q1 = Q1,
                Q2 = Q2,
                Q3 = Q3

            )

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())

