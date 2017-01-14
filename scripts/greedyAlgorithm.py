import csv


class Player():
    def __init__(self, position, name, salary, points, value):
        self.self = self
        self.position = position
        self.positionB = positionB
        self.name = name
        self.salary = salary
        self.points = points
        self.value = value

    def __iter__(self):
        return iter(self.list)

    def __str__(self):
        return "{} {} {} {}".format(self.name, self.position, self.salary, self.points)

# This csv contains our predictions and salaries for each player.
# We parse each row of the csv and convert it into a Player object.
with open('to_knapsackPosY.csv', 'r') as data:
    reader = csv.reader(data)
    reader.next()
    players = []
    for row in reader:
        name = row[0]
        position = row[1]
        positionB = row[2]
        salary = int(row[3])
        points = float(row[4])
        value = points / salary
        player = Player(position, name, salary, points, value)
        players.append(player)


def improved_knapsack(players):
    budget = 66400000
    current_team_salary = 0
    constraints = {
        'RW': 3,
        'C': 3,
        'LW': 3,
        'D': 6,
        'UTIL': 3
    }

    counts = {
        'RW': 0,
        'C': 0,
        'LW': 0,
        'D': 0,
        'UTIL': 0
    }

    players.sort(key=lambda x: x.value, reverse=True)
    team = []

    for player in players:
        nam = player.name
        pos = player.position
        posB = player.positionB
        sal = player.salary
        pts = player.points
        if counts[pos] < constraints[pos]  and current_team_salary + sal <= budget:
            team.append(player)
            counts[pos] = counts[pos] + 1
            current_team_salary += sal
            continue
        elif counts[posB] < constraints[posB]  and current_team_salary + sal <= budget:
            team.append(player)
            counts[posB] = counts[posB] + 1
            current_team_salary += sal
            continue
        if counts['UTIL'] < constraints['UTIL'] and current_team_salary + sal <= budget and pos in ['LW', 'C', 'RW', 'D']:
            team.append(player)
            counts['UTIL'] = counts['UTIL'] + 1
            current_team_salary += sal

    players.sort(key=lambda x: x.points, reverse=True)
    for player in players:
        nam = player.name
        pos = player.position
        sal = player.salary
        pts = player.points
        if player not in team:
            pos_players = [x for x in team if x.position == pos]
            pos_players.sort(key=lambda x: x.points)
            for pos_player in pos_players:
                if (current_team_salary + sal - pos_player.salary) <= budget and pts > pos_player.points:
                    team[team.index(pos_player)] = player
                    current_team_salary = current_team_salary + sal - pos_player.salary
                    break
    return team

team = improved_knapsack(players)
points = 0
salary = 0
output_file = csv.writer(open('result.csv','wb'))
for player in team:
    points += player.points
    salary += player.salary
    print player
    output_file.writerow([player.name, salary])

print "\nPoints: {}".format(points)
print "Salary: {}".format(salary)



