create table nfl.teams(
	id varchar(36) not null default (UUID()),
    location varchar(25) not null,
    team_name varchar(25),
    create_date datetime not null default current_timestamp,
    update_date datetime not null default current_timestamp,
    primary key (id)
    )
comment = 'Stores Team Names'
;
use nfl;
create trigger teams_update_date before update on nfl.teams
	for each row
    set new.update_date = current_timestamp
;
CREATE UNIQUE INDEX unique_teams_index
ON teams (location, team_name);

create table nfl.games(
	id varchar(36) not null default (UUID()),
    game_date datetime not null,
    home_team varchar(36),
    home_line float,
    away_team varchar(36),
    away_line float,
    over_under float,
    create_date datetime not null default current_timestamp,
    update_date datetime not null default current_timestamp,
    primary key (id),
	foreign key (home_team) references nfl.teams(id),
	foreign key (away_team) references nfl.teams(id)
    )
comment = 'Stores the game and its odds'
;
create trigger games_update_date before update on nfl.games
	for each row
    set new.update_date = current_timestamp
;
CREATE UNIQUE INDEX unique_games_index
ON games (game_date, home_team, away_team);

create table nfl.game_scores(
	id varchar(36) not null default (UUID()),
    game_id varchar(36),
    period int,
    home_score int,
    away_score int,
	create_date datetime not null default current_timestamp,
    update_date datetime not null default current_timestamp,
    primary key (id),
	foreign key (game_id) references nfl.games(id)
    )
comment = 'Stores the result of a game'
;
create trigger game_scores_update_date before update on nfl.game_scores
	for each row
    set new.update_date = current_timestamp
;
CREATE UNIQUE INDEX unique_game_scores_index
ON game_scores (game_id, period);

-- TEMPLATE --
-- create table nfl.(
-- id varchar(36) not null default (UUID()),
-- create_date datetime not null default current_timestamp,
-- update_date datetime not null default current_timestamp,
-- primary key (id),
-- foreign key (create_user) references user_acl.user(id),
-- foreign key (update_user) references user_acl.user(id)
-- comment = ''
-- ;
-- create trigger _update_date before update on nfl.
-- 	for each row
--     set new.update_date = current_timestamp
-- ;