from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import parse_utils
import db_utils

URL = "https://www.pro-football-reference.com/years/2025/week_3.htm"
games = parse_utils.ParseHTML.URLTagsClass(URL, "table", "teams")
box_links = []
team_ids = db_utils.Queries.getTeamIds()
game_data = []

for game in games:
    data = game.find_all("tr")
    date_split = data[0].text.replace(',', '').split(' ')
    teams = data[1]
    team_data = teams.find_all("td")
    box_links.append(team_data[2].find("a").get("href"))

firefox_options = Options()
firefox_options.add_argument("--headless=new")
driver = webdriver.Firefox(options = firefox_options)

for box_link in box_links:
    URL = "https://www.pro-football-reference.com" + box_link
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scorebox = soup.find("div", "scorebox")
    teams = scorebox.find_all("a")
    # For 1st week of season, games have no previous game button so have to add offset
    offset = len(scorebox.find_all("div", "prevnext")[0].find_all("a"))
    away_team = team_ids[teams[2].text]
    home_team_text = teams[6 + offset].text
    home_team = team_ids[home_team_text]
    scorebox_meta = soup.find("div", "scorebox_meta").find_all("div")
    game_date = scorebox_meta[0].text.replace(',', '').split(' ')
    game_date[1] = parse_utils.ParseMonth.parse(game_date[1])
    time_text = scorebox_meta[1].text.split(' ')[2]
    convert_time = datetime.strptime(time_text, "%I:%M%p")
    convert_24hr = datetime.strftime(convert_time, "%H:%M")
    time_vals = convert_24hr.split(':')
    game_date_time = datetime(int(game_date[3]), game_date[1], int(game_date[2]),
                              int(time_vals[0]), int(time_vals[1]))
    game_info = soup.find("table", id="game_info")
    game_odds = game_info.find_all("tr")
    # This table changes length, but odds data is always last 2 elements
    line = game_odds[-2].find("td").text
    over_under = game_odds[-1].find("td").text.split(' ')[0]
    favorite = ["NONE", 0.0] if line == "Pick" else line.rsplit(' ', 1) 
    home_line = (float(favorite[1]) if favorite[0] == home_team_text
                 else abs(float(favorite[1])))
    away_line = -home_line
    game_data.append((game_date_time, home_team, home_line,
                      away_team, away_line, over_under))

db_utils.Queries.insertGames(game_data)
driver.quit()
print("DONE!!")

