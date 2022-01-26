import scrapy
from scrapy import Request
from ..items import ArticleItem

class F1Spider(scrapy.Spider):
    name = "f1fca"
    allowed_domains = ["www.f1cfa.com"]
    start_urls = ["https://www.f1cfa.com/f1-tyres-statistics.asp?t=2012&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2013&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2014&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2015&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2016&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2017&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2018&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2019&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2020&gpn=All&tipo=All&driver=All",
                  "https://www.f1cfa.com/f1-tyres-statistics.asp?t=2021&gpn=All&tipo=All&driver=All"]
   

    def parse(self, response):
        title = response.css('#centraralgo h1::text').extract_first()
        for article in response.css('#circuitos').css("tr")[1:]:
            Driver = article.css("td::text").extract_first()
            GP = article.css('td a::text').extract_first()
            Tyres = article.css("td::text")[1].extract()
            Lap_changed= article.css(".SinColor")[1].css("td::text").extract_first()
            yield ArticleItem(
                    title = title,
                    Driver = Driver,
                    GP = GP,
                    Tyres = Tyres,
                    Lap_changed = Lap_changed

                )


    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())

"""  
yield {
            "title":title,
            "all_links":all_links
        }
        
        
        
        
        
        
        
        
        
        
        """