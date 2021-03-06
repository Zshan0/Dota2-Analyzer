import click
from click_shell import shell
import db_conn

# Class to handle shell exiting
class OnExit():

    def __call__(self, garbage):
        click.secho('Goodbye', fg='green')


# Callable executed on shell exit
on_shell_exit = OnExit()


@shell(prompt='dotabase > ', intro='Welcome to Dotabase...', on_finished=on_shell_exit)
def dota():	
	host = click.prompt(db_conn.format_att("host", "green"), type=str)
	user = click.prompt(db_conn.format_att("user", "green"), type=str)
	password = click.prompt(db_conn.format_att("password", "green"),
                type=str, default='')
	db_conn.db_connect(host, user, password)


@dota.command()
def list_tables():
    '''Lists available tables in database'''
    print("Listing available tables")
    db_conn.list_tables()


@dota.command()
@click.argument('table')
def insert(table):
    '''Insert data into the corresponding TABLE'''
    db_conn.insert(table)


@dota.command()
@click.argument('table')
def delete(table):
    '''Delete data from the corresponding TABLE'''
    db_conn.delete(table)


@dota.command()
@click.argument('table')
def modify(table):
    '''Modify data from a corresponding TABLE'''
    db_conn.modify(table)

# --- Retrival Commands Start ---


@dota.group()
def retrieve():
    '''Retrieval commands on database'''
    pass


# --- Select Commands Start ---

@retrieve.group()
def select():
    '''Selection commands on database'''
    pass


@select.command()
@click.argument('team')
def team_matches(team):
    '''Get all matches played by a team'''
    db_conn.team_matches(team)


@select.command()
@click.argument('player')
def player_match(player):
    '''Get all matches player by a player'''
    db_conn.player_matches(player)


@select.command()
@click.argument('team1')
@click.argument('team2')
def match_against(team1, team2):
    '''Get all matches played between 2 given teams'''
    db_conn.match_against(team1, team2)

# --- Select Commands End ---

# --- Project Commands Start ---


@retrieve.group()
def project():
    '''Projection commands on database'''
    pass


@project.command()
@click.argument('player')
@click.argument('x')
def winrate_greater_player(player, x):
    '''Get all Heroes with win-rate >= x, for a certain player'''
    db_conn.winrate_greater_player(player, x)


@project.command()
@click.argument('x')
def winrate_greater(x):
    '''Get all Heroes with win-rate >= x'''
    db_conn.winrate_greater(x)

# --- Project Commands End ---

# --- Aggregate Commands Start ---


@retrieve.group()
def aggregate():
    '''Commands for doing aggregate operations on database'''
    pass


@aggregate.command()
@click.argument('player')
@click.argument('primary_att')
def wins_by_pattr(player, primary_att):
    '''Total wins by a player for all heroes of a given primary attribute'''
    db_conn.wins_by_pattr(player, primary_att)

@aggregate.command()
@click.argument('player')
def total_time(player):
    '''Total time by a player in all the matches'''
    db_conn.total_time(player)


@aggregate.command()
@click.argument('player')
def total_wins(player):
    '''Total wins by player in all the matches'''
    db_conn.total_wins(player)

# --- Aggregate Commands End

# --- Search Commands Start


@retrieve.group()
def search():
    '''Commands for doing partial search on database'''
    pass


@search.command()
@click.argument('hero')
def find_hero(hero):
    '''Get info about a hero. Supports partial text match'''
    db_conn.find_hero(hero)


@search.command()
@click.argument('player')
def find_player(player):
    '''Get info about a player. Supports partial text match'''
    db_conn.find_player(player)

# --- Search Commands End

# --- Retrival Commands End

# --- Analysis Commands Start


@dota.group()
def analysis():
    '''Commands related to generating analysis reports'''
    pass


@analysis.command()
def player_report():
    '''Generate a report of all the players based on their wins'''
    db_conn.player_report()


@analysis.command()
def team_report():
    '''Generate a report on performance of all the teams based on history'''
    db_conn.team_report()


@analysis.command()
@click.argument('option')
def tour_report(option):
    '''Generate a report of the tournaments'''
    db_conn.tournament_report(option)


@analysis.command()
def hero_report():
    '''Generate a report on all the heroes'''
    db_conn.hero_report()

# --- Analysis Commands End ---


if __name__ == '__main__':
    dota()
