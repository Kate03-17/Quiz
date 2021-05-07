import json
import sqlite3 as sql
import requests as req
import json as js
# out of request module functions we use status_code, get, text and json()


url = "https://www.balldontlie.io/api/v1/players"
resp = req.get(url)
res = js.loads(resp.text)
with open('data.json', 'w') as f:
    json.dump(res, f, indent=4)

# in this block we take the information about NBA players and their teams using APi and
# write them in a file reformatting the text for better visibility


conn = sql.connect("favorites.sqlite3")
c = conn.cursor()

c.execute('''create table if not exists favorite_players(id integer, fname varchar(20), lname varchar(20), team_name varchar(20))''')
c.execute("""create table if not exists favorite_teams(id integer, name varchar(20), abbr varchar(10), city varchar(20))""")

# here we connect to the new database and create two tables, one for favorite players, one for favorite teams


def add_new_players(list):
    c.executemany("insert into favorite_players(id, fname, lname, team_name) values(?, ?, ?, ?)", list)
    conn.commit()


def add_new_teams(list):
    c.executemany("insert into favorite_teams(id, name, abbr, city) values(?, ?, ?, ?)", list)
    conn.commit()


# functions that inserts data about chosen favorite players or teams into the corresponding table
# (in case user entered 2 or more data at the same time)
# better explained below


def add_new_player(tuple):
    c.execute("insert into favorite_players(id, fname, lname, team_name) values(?, ?, ?, ?)", tuple)
    conn.commit()


def add_new_team(tuple):
    c.execute("insert into favorite_teams(id, name, abbr, city) values(?, ?, ?, ?)", tuple)
    conn.commit()

# functions that inserts data about chosen favorite player or team into the corresponding table
# (in case user entered only 1 data)
# better explained below


def get_new_players(full_name):
    url_players = f"https://www.balldontlie.io/api/v1/players?search={full_name}"
    resp = req.get(url_players)
    if resp.status_code == 200:
        res = js.loads(resp.text)
        data = res['data'][0]
        result = (data['id'], data['first_name'], data['last_name'], data['team']['name'])
        return result
    else:
        print(resp.status_code)


def get_new_teams(team_id):
    url_teams = f"https://www.balldontlie.io/api/v1/teams/{team_id}"
    resp = req.get(url_teams)
    if resp.status_code == 200:
        res = js.loads(resp.text)
        result = (res['id'], res['name'], res['abbreviation'], res['city'])
        return result
    else:
        print(resp.status_code)


# functions that get the information about specific players(by their name) or teams(by their id) using API

player_list = []
team_list = []
init_inp = input("Do you wish to add a player or a team? ").lower()
count = int(input("How many do you want to add: "))
if init_inp == 'player':
    if count != 1:
        for i in range(0, count):
            name = input('please enter full name of the player: ')
            new = get_new_players(name)
            print(f"information: {new}")
            player_list.append(new)
        add_new_players(player_list)
    else:
        name = input('please enter full name of the player: ')
        new = get_new_players(name)
        print(f"information: {new}")
        add_new_player(new)

elif init_inp == 'team':
    if count != 1:
        for i in range(0, count):
            id = input('please enter id of the team: ')
            new = get_new_teams(id)
            print(f"information: {new}")
            team_list.append(new)
        add_new_teams(team_list)
    else:
        id = input('please enter id of the team: ')
        new = get_new_teams(id)
        print(f"information: {new}")
        add_new_team(new)
else:
    print('invalid input')

# here we let the user add new players or teams,
# in case user chooses to enter 1 name or id we use execute
# in case user chooses to enter more than 1 name or id we use executemany
# we also print the information taken from API here (objective N3)

# example names for test input: MarShon Brooks, Lorenzo Brown, Alex Abrines, Tyler Davis, Keenan Evans
# example ids for text input: anything in range(5...30) including 30.
# first 4 are already in base and will repeat upon repeated input













