from bs4 import BeautifulSoup

def get_project_links(base_url, html):
    soup = BeautifulSoup(html, features="lxml")

    results_div = soup.find('div', id='results')
    data_divs = results_div.find_all('div', class_='data')

    links = []
    for data_div in data_divs:
        links.append(f'{base_url}{data_div.find('div').find('a')['href']}')
    print(links)
    return links

def extract_data(base_url, html):
    data = {}
    soup = BeautifulSoup(html, features="lxml")

    data['title'] = soup.title.string

    description_title_element = soup.find('h3', string='Allgemeine Vorhabenbeschreibung')
    description = description_title_element.find_next_sibling('p').string
    data['description'] = description

    download_link = soup.find('a', title='Alle Dokumente als ZIP-Datei herunterladen')['href']
    data['download_link'] = download_link
    
    print(data)
    return data, soup.prettify()