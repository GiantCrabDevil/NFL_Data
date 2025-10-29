create table nfl.teams(
	id varchar(36) not null default (UUID()),
    location varchar(25) not null,
    team_name varchar(25),
    create_date datetime not null default current_timestamp,
    update_date datetime not null default current_timestamp,
    primary key (id)
    )
comment = ''
;
use nfl;
create trigger teams_update_date before update on nfl.teams
	for each row
    set new.update_date = current_timestamp
;

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
    primary key (id)
    )
comment = ''
;
create trigger games_update_date before update on nfl.games
	for each row
    set new.update_date = current_timestamp
;

-- TEMPLATE --
-- create table nfl.(
-- 	id varchar(36) not null default (UUID()),
-- 	create_date datetime not null default current_timestamp,
--     create_user varchar(36) not	null,
--     update_date datetime not null default current_timestamp,
--     update_user varchar(36) not	null,
--     primary key (id),
-- foreign key (create_user) references user_acl.user(id),
-- foreign key (update_user) references user_acl.user(id)
-- comment = ''
-- ;
-- create trigger _update_date before update on recipe.
-- 	for each row
--     set new.update_date = current_timestamp
-- ;