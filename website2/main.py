from SeleniumDriver import SeleniumDriver
from utils import save_data

def main():
    url = r'https://edl.doe.gov.my/discovery?query=+where+category%3d+%2527EIA+Report%2527&category=EIA%20Report&main=Digital'
    selenium_driver = SeleniumDriver()
    selenium_driver.open(url)
    
    for page in range(1,6):
        selenium_driver.navigate_to_page_number(page)
        projects = selenium_driver.get_projects()

        for index, project in enumerate(projects):
            selenium_driver.navigate_to_project(index)
            data, pretty_html = selenium_driver.extract_data()
            save_data.save('website2/output', data, pretty_html, page, index)
            selenium_driver.open(url)
    
    selenium_driver.close()
    

if __name__ == "__main__":
    main()