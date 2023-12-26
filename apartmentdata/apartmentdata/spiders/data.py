from pathlib import Path
import scrapy
import pandas as pd


class QuotesSpider(scrapy.Spider):
    name = "data"

    start_urls = [
            "https://www.sobha.com/residential/",
        ]
    
    def __init__(self):
        self.file_count = 1

    def _parse(self, response):

        link_to_follow = response.css('.select-wrapper select option::attr(value)').getall()[1:]
        for link in link_to_follow:
            yield scrapy.Request(url=link, callback=self.parse_html_page)

    def parse_html_page(self, response):
        items = []
        page_name = response.url.split("/")[-2]

        for data in response.css("div.col-md-6.col-6.pr-md-5.mb-md-5.mb-4"):
            item = {
                "Apartmentname": data.css("h2 a::text").get(),
                "Addresss": data.css("h3::text").getall(),
                "Availability": data.css("span.units::text").get()
            }
            items.append(item)

        # Convert the list of items into a Pandas DataFrame
        df = pd.DataFrame(items)
        file_name = f"{self.file_count}_{page_name}.csv"
        df.to_csv(file_name, index=False)
        self.file_count += 1