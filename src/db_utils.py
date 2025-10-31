from mysql.connector import connection

class Queries:

    db_config = {
        'user' : 'Damon',
        'password' : 'jRdM0307',
        'host' : 'localhost',
        'database' : 'nfl'
        }

    @classmethod
    def insertGames(cls, data):
        query = """
        insert into games
        (game_date, home_team, home_line, away_team, away_line, over_under)
        values(%s, %s, %s, %s, %s, %s);
        """
        cls.insert(query, data)
        
    @classmethod
    def getTeamIds(cls):
        query = """
        select concat(location, ' ', team_name) as team, id
        from teams
        """
        conn = connection.MySQLConnection(**cls.db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        teams = {}
        for(team, id) in cursor:
            teams[team] = id
        cursor.close()
        conn.close()
        return teams

    @classmethod
    def getGameId(cls, home_team, away_team, date):
        query = """
        select id
         from games
         where home_team = %s
         and away_team = %s
         and game_date = %s
        """
        conn = connection.MySQLConnection(**cls.db_config)
        cursor = conn.cursor()
        cursor.execute(query, (home_team, away_team, date))
        game_id = cursor.fetchone()
        cursor.close()
        conn.close()
        return game_id
    
    @classmethod
    def insertGameScores(cls, data):
        query = """
        insert into game_scores
        (game_id, period, home_score, away_score)
        values(%s, %s, %s, %s)
        """
        cls.insert(query, data)

    @classmethod
    def insert(cls, query, data_rows):
        conn = connection.MySQLConnection(**cls.db_config)
        cursor = conn.cursor()
        for data in data_rows:
            cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
