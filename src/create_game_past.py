import cloudscraper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from mysql.connector import connection
from datetime import date, datetime, time

URL = "https://www.pro-football-reference.com/years/2025/week_7.htm"
scraper = cloudscraper.create_scraper()
response = scraper.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
games = soup.find_all("table", class_="teams")
box_links = []
dates = []
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

for game in games[:1]:
    data = game.find_all("tr")
    date_split = data[0].text.replace(',', '').split(' ')
    dates.append(date(int(date_split[2]), date_dict[date_split[0]], int(date_split[1])))
    teams = data[1]
    team_data = teams.find_all("td")
    box_links.append(team_data[2].find("a").get("href"))

firefox_options = Options()
firefox_options.add_argument("--headless=new")
driver = webdriver.Firefox(options = firefox_options)

db_config = {
    'user' : 'Damon',
    'password' : 'jRdM0307',
    'host' : 'localhost',
    'database' : 'nfl'
    }

conn = connection.MySQLConnection(**db_config)
cursor = conn.cursor()
query = ("select concat(location, ' ', team_name) as team, id from teams")
cursor.execute(query)
team_dict = {}
for(team, id) in cursor:
    team_dict[team] = id

for box_link in box_links:
    URL = "https://www.pro-football-reference.com" + box_link
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scorebox_meta = soup.find("div", "scorebox_meta")
    lines = scorebox_meta.find_all("div")
    time_text = lines[1].text.split(' ')[2]
    convert_time = datetime.strptime(time_text, "%I:%M%p")
    convert_24hr = datetime.strftime(convert_time, "%H:%M")
    time_vals = convert_24hr.split(':')
    game_time = time(int(time_vals[0]), int(time_vals[1]))

    
    scorebox = soup.find("div", "scorebox")
    teams = scorebox.find_all("a")
    away_team = team_dict[teams[2].text]
    home_team = team_dict[teams[8].text]
    game_info = soup.find("table", id="game_info")
    game_data = game_info.find_all("tr")
    line = game_data[7].find("td").text
    over_under = game_data[8].find("td").text.split(' ')[0]
    favorite = line.rsplit(' ', 1) 
    home_line = float(favorite[1]) if favorite[0] == home_team else abs(float(favorite[1]))
    away_line = -home_line
 
    game_date_time = datetime.combine(dates.pop(0), game_time)
    game_data = (game_date_time, home_team, home_line, away_team, away_line, over_under)

    insert = """
    insert into games
    (game_date, home_team, home_line, away_team, away_line, over_under)
    values(%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert, game_data) 
    print(away_team)
    print(away_line)
    print(home_team)
    print(home_line)
    print(over_under)
    print(date)

driver.quit()
conn.commit()
cursor.close()
conn.close()
