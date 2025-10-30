import cloudscraper
from bs4 import BeautifulSoup

class ParseMonth:

    @staticmethod
    def parse(month):
        date_dict = {}
        date_dict['Jan'] = 1
        date_dict['Feb'] = 2
        date_dict['Mar'] = 3
        date_dict['Apr'] = 4
        date_dict['May'] = 5
        date_dict['Jun'] = 6
        date_dict['Jul'] = 7
        date_dict['Aug'] = 8
        date_dict['Sep'] = 9
        date_dict['Oct'] = 10
        date_dict['Nov'] = 11
        date_dict['Dec'] = 12
        return date_dict[month]

class ParseHTML:

    @staticmethod
    def URL(url):
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        return BeautifulSoup(response.content, "html.parser")

    @staticmethod
    def URLTagsClass(url, tag, class_name):
        return ParseHTML.URL(url).find_all(tag, class_name)

    @staticmethod
    def URLTagClass(url, tag, class_name):
        return ParseHTML.URL(url).find(tag, class_name)
        
