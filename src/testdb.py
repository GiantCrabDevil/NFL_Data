from mysql.connector import connection
from datetime import date


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


date_string = "Oct 16, 2025"
date_split = date_string.replace(',', '').split(' ')
#date_split = no_comma.split(' ')
game_date = date(int(date_split[2]), date_dict[date_split[0]], int(date_split[1]))

print(game_date)


cursor.close()
conn.close()
