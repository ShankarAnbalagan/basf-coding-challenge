import scrapy
from urllib.parse import urlparse, parse_qs
import time

import website1_scrape
from utils import save_data

class Website1Spider(scrapy.Spider):
    name = "website1"

    def start_requests(self):
        urls = list((f"https://www.uvp-verbund.de/freitextsuche?rstart=0&currentSelectorPage={page_number}" for page_number in range(1, 6)))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            time.sleep(5)

    def parse(self, response):
        parsed_url = urlparse(response.url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        project_links = website1_scrape.get_project_links(base_url, response.body)
        for index, link in enumerate(project_links):
            yield scrapy.Request(url=link, callback=self.parse_project, meta={'index': index})
            time.sleep(5)
    
    def parse_project(self, response):
        project_index = response.meta['index']

        project_url = response.url
        parsed_url = urlparse(response.url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        page_num = parse_qs(parsed_url.query)['currentSelectorPage'][0]

        project_data, project_html = website1_scrape.extract_data(base_url, response.body)
        save_data.save('website1\output', project_data, project_html, page_num, project_index)