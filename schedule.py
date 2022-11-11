import random
from schedule_list import *

for k, v in teams.items():
    x = teams[k]["3"]
    random.shuffle(x)
    teams[k]["3"] = x

    x = teams[k]["4"]
    random.shuffle(x)
    teams[k]["4"] = x

days = {}

games = 42
days_off = 10
x = "3"

for i in range(180):
    if i + 1 in days:
        continue
    if 105 < i+1 < 114:
        days[i+1] = "All star break!"
        continue
    if random.randint(1, 4) == 1 and days_off > 0:
        days[i+1] = "Day off."
        days_off -= 1
        continue

    day_schedule = []

    if games % 5 == 0 and x == "3": x = "4"
    else: x = "3"

    threshold = games if x == "3" else int(games / 5)+1

    for team, sched in teams.items():
        if len(sched[x]) >= threshold:
            for j, opp in enumerate(sched[x]):
                if len(teams[opp][x]) >= threshold:
                    day_schedule.append(f"{opp} vs {team}")
                    teams[opp][x].remove(team)
                    del sched[x][j]
                    break

    days[i + 1] = day_schedule
    days[i + 2] = day_schedule
    days[i + 3] = day_schedule
    if x == "4":
        days[i + 4] = day_schedule

    if x == "3":
        games -= 1

for k, v in days.items():
    print(f"{k}: {v}")