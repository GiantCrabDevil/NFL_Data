import cloudscraper
from bs4 import BeautifulSoup
from mysql.connector import connection
from datetime import date, datetime, time
import parse_utils
import db_utils

games = parse_utils.ParseHTML.URLTagsClass("https://www.pro-football-reference.com/years/2025/week_9.htm",
                                           "table", "teams")
box_links = []
team_ids = db_utils.Queries.getTeamIds()
game_data = []

for game in games:
    data = game.find_all("tr")
    teams = data[1]
    team_data = teams.find_all("td")
    box_links.append(team_data[2].find("a").get("href"))

for box_link in box_links:
    soup = parse_utils.ParseHTML.URL("https://www.pro-football-reference.com" + box_link)
    teams = soup.find("div", "scorebox").find_all("a")
    away_team = team_ids[teams[2].text]
    home_team_text = teams[8].text
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
    line = scorebox_meta[3].text.rsplit(' ', 1)
    favorite = line[0].split(': ')[1]
    home_line = float(line[1]) if favorite in home_team_text else abs(float(line[1]))
    away_line = -home_line
    over_under = scorebox_meta[4].text.split(' ')[1]
    game_data.append((game_date_time, home_team, home_line,
                      away_team, away_line, over_under))

db_utils.Queries.insertGames(game_data)
print("DONE!")
        
