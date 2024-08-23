from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

class SeleniumDriver:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_experimental_option("detach", True)
        service = webdriver.ChromeService(executable_path=r'website2\chromedriver.exe')
        self._driver = webdriver.Chrome(service=service, options=chrome_options)

    def close(self):
        self._driver.close()

    def open(self, url):
        self._driver.get(url)

    def navigate_to_page_number(self, page_num):
        id = f'content_body_rptPaging_lbPaging_{page_num - 1}'
        WebDriverWait(self._driver, 30).until(expected_conditions.presence_of_element_located((By.ID, id)))
        next_page_a = self._driver.find_element(By.ID, id)
        self._driver.execute_script('arguments[0].click();', next_page_a)

    def navigate_to_project(self, project_index):
        print(f'content_body_rptResult_lbtnOverview2_{project_index}')
        element = self._driver.find_element(By.ID, f'content_body_rptResult_lbtnOverview2_{project_index}')
        self._driver.execute_script('arguments[0].click();', element)

    def get_projects(self):
        project_elements = self._driver.find_elements(By.CLASS_NAME, 'lbltitle_')
        return project_elements
    
    def get_page_html(self):
        return self._driver.page_source
    
    def _get_data_by_id(self, soup, id):
        return soup.find('textarea', id=id).string
    
    def extract_data(self):
        WebDriverWait(self._driver, 30).until(expected_conditions.presence_of_element_located((By.ID, 'content_body_txtTitle')))

        data = {}
        soup = BeautifulSoup(self._driver.page_source, features="lxml")
        
        data['title'] = self._get_data_by_id(soup, 'content_body_txtTitle')
        data['category'] = self._get_data_by_id(soup, 'content_body_txtsubcategory')
        data['release_date'] = self._get_data_by_id(soup, 'content_body_txtreleased_eia')
        data['consultant'] = self._get_data_by_id(soup, 'content_body_txtconsultant_eia')
        data['project_developer'] = self._get_data_by_id(soup, 'content_body_txtconsultant_eia')
        data['location'] = self._get_data_by_id(soup, 'content_body_txtlocation_eia')
        data['post_date'] = soup.find('input', id='content_body_txtdatepost_eia')['value']


        # https://edl.doe.gov.my/images/items/42681/attachment/20241908131633413.pdf
        page_url = self._driver.current_url
        parsed_url = urlparse(page_url)
        download_base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/images/items/"
        bib_number = parse_qs(parsed_url.query)['bibnumber'][0]

        download_links = []
        download_a_tags = soup.find_all('a', class_='lbtn')
        for tag in download_a_tags:
            download_links.append(f'{download_base_url}{bib_number}/attachment/{tag.string}')
        data['download_links'] = download_links

        print(data)
        return data, soup.prettify()    