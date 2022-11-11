import random

pitch_dict = {
    (3, 0): [0.84, 0.08, 0.08],
    (3, 1): [0.80, 0.13, 0.07],
    (2, 0): [0.75, 0.15, 0.10],
    (3, 2): [0.66, 0.25, 0.09],
    (1, 0): [0.64, 0.23, 0.13],
    (2, 1): [0.64, 0.24, 0.13],
    (0, 0): [0.63, 0.27, 0.10],
    (1, 1): [0.53, 0.32, 0.15],
    (0, 1): [0.52, 0.35, 0.12],
    (2, 2): [0.51, 0.37, 0.12],
    (1, 2): [0.48, 0.41, 0.11],
    (0, 2): [0.51, 0.39, 0.10],
}

swing = {
    False: {
        "ahead": [0.215, 0.256, 0.317],
        "even": [0.188, 0.214, 0.316],
        "behind": [0.285, 0.332, 0.366],
    },
    True: {  # inside zone
        "ahead": [0.700, 0.567, 0.747],  # ahead for the hitter ie 3-0 count
        "even": [0.607, 0.475, 0.727],
        "behind": [0.820, 0.780, 0.869],
    },
}  # MAKE FOR 2 STRIKE COUNT

zone = {
    (0, 0): [0.564, 0.496, 0.530],
    (0, 1): [0.488, 0.425, 0.457],
    (0, 2): [0.363, 0.297, 0.330],
    (1, 2): [0.433, 0.345, 0.389],
    (1, 0): [0.582, 0.512, 0.547],
    (1, 1): [0.537, 0.480, 0.508],
    (2, 1): [0.587, 0.515, 0.551],
    (2, 2): [0.524, 0.415, 0.470],
    (2, 0): [0.605, 0.503, 0.554],
    (3, 0): [0.658, 0.675, 0.667],  # 628, 645, 637
    (3, 1): [0.513, 0.523, 0.518],  # 483, 493, 488
    (3, 2): [0.653, 0.537, 0.595],  # 623, 507, 565
}

# 1st number is fastball%, breaking%, offspeed%

outcomes = {
    False: {  # outside zone
        "foul": [0.355, 0.229, 0.238],
        "whiff": [0.318, 0.548, 0.411],
        "bip": [0.327, 0.223, 0.350],
    },
    True: {  # inside zone
        "foul": [0.363, 0.308, 0.281],
        "whiff": [0.180, 0.168, 0.215],
        "bip": [0.457, 0.524, 0.505],
    },
}

babip = {
    True: [0.343, 0.327, 0.318],  # inside zone
    False: [0.290, 0.287, 0.267]
}

exp_hit = {
    True: [0.625, 0.205, 0.017, 0.153],
    False: [0.700, 0.159, 0.013, 0.127]
}  # 1b 2b 3b hr probability

class Simulation:
    def __init__(self):
        self.bases = {1: False, 2: False, 3: False}
        self.runs = {"team1": 0, "team2": 0}
        self.inning = 1
        self.top = True
        self.balls = 0
        self.strikes = 0
        self.outs = 0
        self.at_bat = True

        self.plateappearances = 1
        self.hits = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.homeruns = 0
        self.sacflies = 0
        self.stolenbases = 0
        self.caughtstealing = 0
        self.chances = 0
        self.errors = 0

        self.walks = 0
        self.ks = 0
        self.whiffs = 0
        self.pitches = 0
        self.swings = 0
        self.fouls = 0
        self.s = 0
        self.hbp = 0
        self.total_ball_thrown = 0
        self.total_strike_thrown = 0

    def advance(team, amount, hit=False):
        global outs
        for base in [3, 2, 1]:
            if outs == 3: break
            if bases[base]:
                if base == 1 and amount == 1 and hit:
                    if bases[3]:
                        bases[2] = True
                    else:
                        outcome = random.choices(population=["third", "second", "out"], weights=[0.25, 0.7, 0.05])[0]
                        if outcome == "third":
                            bases[3] = True
                        elif outcome == "second":
                            bases[2] = True
                        else:
                            outs += 1

                elif ((amount == 2 and base == 1) or (amount == 1 and base == 2)) and hit:
                    outcome = random.choices(population=["home", "third", "out"], weights=[0.4, 0.5, 0.1])[0]
                    if outcome == "home":
                        runs[team] += 1
                    elif outcome == "third":
                        bases[3] = True
                    else:
                        outs += 1

                else:
                    if base + amount <= 3:
                        bases[base + amount] = True
                    else:
                        runs[team] += 1
                bases[base] = False

