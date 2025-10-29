import cloudscraper
from bs4 import BeautifulSoup
from mysql.connector import connection

URL = "https://www.pro-football-reference.com/years/2025/week_7.htm"
scraper = cloudscraper.create_scraper()
response = scraper.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
games = soup.find_all("table", class_="teams")

for game in games[:1]:
    data = game.find_all("tr")
    date = data[0].text
    team1 = data[1]
    team1_data = team1.find_all("td")
    box_link = team1_data[2].find("a").get("href")
    team1_name = team1_data[0].text
    team1_score = team1_data[1].text
    team2 = data[2]
    team2_data = team2.find_all("td")
    team2_name = team2_data[0].text
    team2_score = team2_data[1].text
    print(date)
    print(team1_name)
    print(team1_score)
    print(team2_name)
    print(team2_score)
    print(box_link)
    print("-----------------------")

db_config = {
    'user' : 'Damon',
    'password' : 'jRdM0307',
    'host' : 'localhost',
    'database' : 'recipe'
    }

conn = connection.MySQLConnection(**db_config)

print(conn)

conn.close()
