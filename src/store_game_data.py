import cloudscraper
from bs4 import BeautifulSoup
from mysql.connector import connection

URL = "https://www.pro-football-reference.com/years/2025/week_7.htm"
scraper = cloudscraper.create_scraper()
response = scraper.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
games = soup.find_all("table", class_="teams")
box_links = []

for game in games[:1]:
    data = game.find_all("tr")
    date = data[0].text
    team1 = data[1]
    team1_data = team1.find_all("td")
    box_links.append(team1_data[2].find("a").get("href"))


for box_link in box_links:
    URL = "https://www.pro-football-reference.com" + box_link
    scraper = cloudscraper.create_scraper()
    response = scraper.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    scorebox = soup.find("div", "scorebox")
    teams = scorebox.find_all("a")
    away_team = teams[2]
    away_coach = teams[5]
    home_team = teams[8]
    home_coach = teams[11]
    stadium = teams[12]
    attendance = teams[13]
    
    for team in teams:
        away_team = t
        print(team.text)
