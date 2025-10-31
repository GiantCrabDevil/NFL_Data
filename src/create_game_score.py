from bs4 import BeautifulSoup
from datetime import datetime
import parse_utils
import db_utils

URL = "https://www.pro-football-reference.com/years/2025/week_1.htm"
games = parse_utils.ParseHTML.URLTagsClass(URL, "table", "teams")
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
    scorebox_meta = soup.find("div", "scorebox_meta").find_all("div")
    game_date = scorebox_meta[0].text.replace(',', '').split(' ')
    game_date[1] = parse_utils.ParseMonth.parse(game_date[1])
    time_text = scorebox_meta[1].text.split(' ')[2]
    convert_time = datetime.strptime(time_text, "%I:%M%p")
    convert_24hr = datetime.strftime(convert_time, "%H:%M")
    time_vals = convert_24hr.split(':')
    game_date_time = datetime(int(game_date[3]), game_date[1], int(game_date[2]),
                              int(time_vals[0]), int(time_vals[1]))
    line_scores = soup.find("div", "linescore_wrap").find_all("td")
    # Every overtime period will add 2 rows, need to calculate for that and offset
    # for the home id and additions to the score rows
    num_periods = int(len(line_scores) / 2 - 3)
    add_periods = num_periods - 4
    away_id = team_ids[line_scores[1].text]
    home_id = team_ids[line_scores[4 + num_periods].text]
    game_id = db_utils.Queries.getGameId(home_id, away_id, game_date_time)[0]
    for i in range(num_periods):
        game_data.append((game_id, i+1, int(line_scores[i+9+add_periods].text),
                          int(line_scores[i+2].text)))
    
db_utils.Queries.insertGameScores(game_data)
print("DONE!!")
