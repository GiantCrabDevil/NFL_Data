import cloudscraper
from bs4 import BeautifulSoup
from datetime import date, datetime, time



URL = "https://www.pro-football-reference.com/boxscores/202510160cin.htm"
scraper = cloudscraper.create_scraper()
response = scraper.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
data = soup.find("div", "scorebox_meta")
divs = data.find_all("div")
time_text = divs[1].text.split(' ')[2]
in_time = datetime.strptime(time_text, "%I:%M%p")
out_time = datetime.strftime(in_time, "%H:%M")
print(out_time.hour)
day = date(2025, 1, 5)
time_vals = out_time.split(':')
game_time = time(int(time_vals[0]), int(time_vals[1]))
game_date_time = datetime.combine(day, game_time)
print(game_date_time)
