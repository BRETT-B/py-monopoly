from flask import Flask
from flaskext.mysql import MySQL
from space import Space
from dice import Dice
mysql = MySQL()
# bring in the flask object
app = Flask(__name__)
# Congiguratey the database options
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'monopoly'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# Initiate the app
mysql.init_app(app)

#Make one connection and use it over, and over, and over...
conn = mysql.connect()
# set up a cursor object whihc is what the sql object uses to connect and run queries
cursor = conn.cursor()


spaces = [
   Space(0, 'GO', None, -200),
   Space(1, 'Mediterranean Avenue', 'Brown', 60),
   Space(2, 'Community Chest', None, None),
   Space(3, 'Baltic Avenue', 'Brown', 60),
   Space(4, 'Income Tax', None, 200),
   Space(5, 'Reading Railroad', 'Railroad', 200),
   Space(6, 'Oriental Avenue', 'Light Blue', 100),
   Space(7, 'Chance', None, None),
   Space(8, 'Vermont Avenue', 'Light Blue', 100),
   Space(9, 'Connecticut Avenue', 'Light Blue', 120),
   Space(10, 'Jail', None, None),
   Space(11, 'St. Charles Place', 'Light Pink', 140),
   Space(12, 'Electric Company', 'Utility', 150),
   Space(13, 'States Avenue', 'Light Pink', 140),
   Space(14, 'Virginia Avenue', 'Light Pink', 160),
   Space(15, 'Pennsylvania Railroad', 'Railroad', 200),
   Space(16, 'St. James Place', 'Orange', 180),
   Space(17, 'Community Chest', None, None),
   Space(18, 'Tennessee Avenue', 'Orange', 180),
   Space(19, 'New York Avenue', 'Orange', 200),
   Space(20, 'Free Parking', None, None),
   Space(21, 'Kentucky Avenue', 'Red', 220),
   Space(22, 'Chance', None, None),
   Space(23, 'Indiana Avenue', 'Red', 220),
   Space(24, 'Illinois Avenue', 'Red', 240),
   Space(25, 'B. & O. Railroad', 'Railroad', 200),
   Space(26, 'Atlantic Avenue', 'Yellow', 260),
   Space(27, 'Ventor Avenue', 'Yellow', 260),
   Space(28, 'Water Works', 'Utility', 150),
   Space(29, 'Marvin Gardens', 'Yellow', 280),
   Space(30, 'Jail', None, None),
   Space(31, 'Pacific Avenue', 'Green', 300),
   Space(32, 'North Carolina Avenue', 'Green', 300),
   Space(33, 'Commmunity Chest', None, None),
   Space(34, 'Pennsylvania Avenue', 'Green', 320),
   Space(35, 'Short Line', 'Railroad', None),
   Space(36, 'Chance', None, None),
   Space(37, 'Park Place', 'Blue', 350),
   Space(38, 'Luxury Tax', None, 100),
   Space(39, 'Boardwalk', 'Blue', 400)
]


def get_space(player):
	for space in spaces:
		if player['current_space'] == space.id:
			return space

die = Dice()

player_1 = {
	'rolls': 0,
	'current_space': 0,
	'distance': 0
}
player_2 = {
	'rolls': 0,
	'current_space': 0,
	'distance': 0
}

current_player = player_1

@app.route('/')
def turn():
   	turn = 0
   	while turn < 1000:
   		while True:
   			die_total = die.roll()

		   	if turn % 2 == 0:
		   		board = player_1['current_space']
		   		rolls = player_1['rolls']
		   		distance = player_1['distance']
		   		print "Player 1 rolled: "+str(die_total)
			  	player_1['rolls'] += 1
			   	player_1['current_space'] += die_total
			   	if player_1['current_space'] > 39:
			   		board -= 40
			   	if board == 30:
			   		print "Go To Jail"
			   		board = 10
			   		turn += 1
			   		break
			   	player_1['distance'] += die_total
			   	prop = "%s" % (spaces[board].name)
			   	query = "INSERT INTO rolls VALUES (DEFAULT, '"+str(die_total)+"', '"+str(distance)+"', 'Player 1', '"+str(prop)+"')" 
				cursor.execute(query)
				conn.commit()
			   	print prop
			   	print player_1

		   	else:
		   		board = player_2['current_space']
		   		rolls = player_2['rolls']
		   		distance = player_2['distance']
		   		print "Player 2 rolled: "+str(die_total)
			   	rolls += 1
			   	board += die_total
			   	if board > 39:
			   		board -= 40
			   	if board == 30:
			   		print "Go To Jail"
			   		board = 10
			   		turn += 1
			   		break
			   	distance += die_total
			   	prop = "%s" % (spaces[board].name)
			   	query = "INSERT INTO rolls VALUES (DEFAULT, '"+str(die_total)+"', '"+str(distance)+"', 'Player 2', '"+str(prop)+"')" 
				cursor.execute(query)
				conn.commit()
			   	print prop
			   	print player_2

		   	if not die.doubles:
			   	turn += 1
			   	break
		   	print "Got doubles!"

   	return 'Monopoly!'

if __name__ == "__main__":
	app.run(debug=True)