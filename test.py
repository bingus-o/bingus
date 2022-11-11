import random
import time
import logging

import numpy as np

log = logging.getLogger("my-logger")

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

# 1st number is fastball%, breaking%, offspeed%

bases = {1: False, 2: False, 3: False}
runs = {"team1": 0, "team2": 0}
inning = 1
top = True
balls = 0
strikes = 0
outs = 0
at_bat = True

plateappearances = 1
hits = 0
singles = 0
doubles = 0
triples = 0
homeruns = 0
sacflies = 0
stolenbases = 0
caughtstealing = 0
chances = 0
errors = 0

walks = 0
ks = 0
whiffs = 0
pitches = 0
swings = 0
fouls = 0
s = 0
hbp = 0
total_ball_thrown = 0
total_strike_thrown = 0


def advance(team, amount, hit=False):
    global outs
    for base in [3, 2, 1]:
        if outs == 3: break
        if bases[base]:
            if base == 1 and amount == 1 and hit:
                if bases[3]: bases[2] = True
                else:
                    outcome = random.choices(population=["third", "second", "out"], weights=[0.25, 0.7, 0.05])[0]
                    if outcome == "third": bases[3] = True
                    elif outcome == "second": bases[2] = True
                    else: outs += 1

            elif ((amount == 2 and base == 1) or (amount == 1 and base == 2)) and hit:
                outcome = random.choices(population=["home", "third", "out"], weights=[0.4, 0.5, 0.1])[0]
                if outcome == "home": runs[team] += 1
                elif outcome == "third": bases[3] = True
                else: outs += 1

            else:
                if base + amount <= 3:
                    bases[base + amount] = True
                else:
                    runs[team] += 1
            bases[base] = False


ball_types = ["fastball", "breaking ball", "change up"]

control = 80
velocity = 80
movement = 80

eye = 80
contact = 80
power = 80

speed = 80
aggressiveness = 80


fielding = 80

def calc_diff(probability, x, multiplier):
    old_p = probability
    probability *= 1 + (((x - 80) * multiplier) / 100)
    return probability - old_p, probability


while inning < 21000:
    # if inning%1000 == 0: log.warning(inning)
    if not at_bat:
        balls = 0
        strikes = 0
        at_bat = True
        plateappearances += 1

        if bases == {1: True, 2: False, 3: False}:
            fraction = (7 / 4) if aggressiveness > 80 else (1 / 4)
            will_steal = ((((fraction * (aggressiveness - 80))) + 3) / 100)
            if will_steal >= random.random():
                fraction = (3 / 5) if speed >= aggressiveness else (7 / 5)
                success = ((((fraction * (speed - aggressiveness))) + 85) / 100)
                if success >= random.random():
                    advance("team1" if top else "team2", 1)
                    stolenbases += 1
                else:
                    bases = {1: False, 2: False, 3: False}
                    caughtstealing += 1

    pitch_selection = random.choices(population=ball_types, weights=pitch_dict[(balls, strikes)])[0]
    index = ball_types.index(pitch_selection)

    zone_p = zone[(balls, strikes)][index]
    in_zone = random.choices(population=[True, False], weights=[zone_p, 1 - zone_p])[0]
    if balls == 3 and not in_zone:
        if random.random() <= (control-80)/120:
            in_zone = True

    if in_zone:
        total_strike_thrown += 1
    else:
        total_ball_thrown += 1

        if random.random() < ((-9/40) * (control-80) + 6)/1000:
            hbp += 1
            advance("team1" if top else "team2", 1)
            bases[1] = True
            at_bat = False
            continue

    if balls > strikes:
        choice = "ahead"
    elif balls < strikes:
        choice = "behind"
    else:
        choice = "even"

    swing_p = swing[in_zone][choice][index]
    if in_zone:
        swing_p += swing_p * (((-1/4) * (control - 80)) / 100)
        # more likely to swing if bad control (bc over heart of plate), less likely if good (bc could be like a ball)
        swing_p += swing_p * (((1/4) * (eye - 80)) / 100)
        # more likely to swing if good eye
    else:
        swing_p += swing_p * (((5/4) * (control - 80)) / 100)
        # more likely to swing if good control, less likely if bad
        swing_p += swing_p * (((-5) * (eye - 80)) / 100)

    did_swing = random.choices(population=[True, False], weights=[swing_p, 1 - swing_p])[0]

    if did_swing:
        swings += 1
        foul_p, whiff_p, bip_p = outcomes[in_zone]["foul"][index], outcomes[in_zone]["whiff"][index], \
                                 outcomes[in_zone]["bip"][index]

        if pitch_selection == "fastball":
            difference, foul_p, difference2, whiff_p = calc_diff(foul_p, velocity, 1.5) +calc_diff(whiff_p, velocity, 1)
            bip_p -= difference + difference2

        elif pitch_selection == "change up":
            difference, foul_p, difference2, whiff_p = calc_diff(foul_p, velocity, 0.75) + calc_diff(whiff_p, velocity, 0.5)
            difference3, whiff_p, difference4, foul_p = calc_diff(whiff_p, movement, 1.75) + calc_diff(foul_p, movement, 1.125)
            bip_p -= difference + difference2 + difference3 + difference4

        else:
            difference, whiff_p, difference2, foul_p = calc_diff(whiff_p, movement, 3.25) + calc_diff(foul_p, movement, 2.25)
            bip_p -= difference + difference2

        difference, bip_p = calc_diff(bip_p, contact, 2.25)

        percent_whiff = whiff_p/(whiff_p+foul_p)
        whiff_p -= difference*percent_whiff
        foul_p -= difference*(1-percent_whiff)

        outcome = random.choices(population=["foul", "whiff", "bip"], weights=[foul_p, whiff_p, bip_p])[0]
        if outcome == "bip":
            hit_p = babip[in_zone][index]
            hit_p -= (((velocity - 80) * 0.06) / 100)
            hit_p -= (((movement - 80) * 0.06) / 100)
            hit_p += (((contact - 80) * 0.1) / 100)
            hit = random.choices(population=[True, False], weights=[hit_p, 1 - hit_p])[0]
            if hit:
                hit_weight = exp_hit[in_zone]
                difference, double, difference2, hr = calc_diff(hit_weight[1], power, 1.5) + calc_diff(hit_weight[3], power, 6.25)
                hit_weight = [hit_weight[0]-difference-difference2, double, hit_weight[2], hr]

                hit_type = random.choices(population=[1, 2, 3, 4], weights=hit_weight)[0]
                advance("team1" if top else "team2", hit_type, hit=True)
                if hit_type != 4:
                    bases[hit_type] = True
                else:
                    runs["team1" if top else "team2"] += 1
                hits += 1

                if hit_type == 1:
                    singles += 1
                elif hit_type == 2:
                    doubles += 1
                elif hit_type == 3:
                    triples += 1
                else:
                    homeruns += 1

            else:
                out_p = 0.985+(((3/4)*(fielding-80))/1000)
                chances += 1
                if out_p > random.random():
                    out_type = random.choices(population=["groundout", "flyout", "lineout", "popup"], weights=[0.45, 0.26, 0.22, 0.07])[0]
                    outs += 1
                    if outs <= 2 and any(x is True for x in [bases[2], bases[3]]) and 0.33 >= random.random():
                        if bases[3]:
                            runs["team1" if top else "team2"] += 1
                            bases[3] = False
                            sacflies += 1

                        if bases[2] and outs == 1:
                            bases[2] = False
                            bases[3] = True

                else:
                    advance("team1" if top else "team2", 1)
                    bases[1] = True
                    errors += 1

            at_bat = False

        elif outcome == "whiff":
            whiffs += 1
            strikes += 1
            s += 1
        else:
            fouls += 1
            if strikes < 2:
                strikes += 1
                s += 1

    else:
        if in_zone:
            strikes += 1
            s += 1
        else:
            balls += 1

    if strikes == 3:
        ks += 1
        outs += 1
        at_bat = False

    elif balls == 4:
        advance("team1" if top else "team2", 1)
        bases[1] = True
        at_bat = False
        walks += 1

    if outs == 3:
        inning += 1 if not top else 0
        top = not top
        at_bat = False
        outs = 0
        bases = {1: False, 2: False, 3: False}
    pitches += 1

print("hits:", hits)
print("walks:", walks)
print("plate appearances:", plateappearances)
print("strikeouts:", ks)
print("whiffs:", whiffs)
print("pitches:", pitches)
print("swings:", swings)
print("fouls:", fouls)
print("strikes:", s)
print("homeruns:", homeruns)
print("triples:", triples)
print("doubles:", doubles)
print("singles:", singles)
print("hit by pitch:", hbp)
print("sac flies:", sacflies)
print("stolen bases:", stolenbases)
print("caught stealings:", caughtstealing)
print("errors:", errors)
print("chances:", chances)

at_bats = plateappearances - walks - hbp
print("K%:", round(ks / plateappearances, 3))
print("BA:", round(hits / at_bats, 3))
print("BB%:", round(walks / plateappearances, 3))
print("Swing%:", round(swings / pitches, 2))
print("Whiff%:", round(whiffs / swings, 2))
print("Foul%:", round(fouls / swings, 2))
print("OBP:", round((hits + walks) / plateappearances, 3))
print("Slug%:", round(((homeruns * 4) + (triples * 3) + (doubles * 2) + singles) / at_bats, 3))
print(f"Percentages: Singles {round(singles / hits, 3)} | Doubles {round(doubles / hits, 3)} "
      f"| Triples {round(triples / hits, 3)} | Home Runs {round(homeruns / hits, 3)}")
print(f"Balls/Strikes: {total_ball_thrown}/{total_strike_thrown}")
print("HBP%:", round(hbp / plateappearances, 3))
print("ERA:", round((sum(list(runs.values())) / 2) / 21000 * 9, 2))
print("WHIP:", round(((walks + hits) / 2) / 21000, 2))
print("BB/9:", round((walks / 2) / 21000 * 9, 2))
print("K/9:", round((ks / 2) / 21000 * 9, 2))
print("SB%:", round(stolenbases/(stolenbases+caughtstealing), 3))
print("FLD%:", round((chances-errors)/chances, 3))
print("SBA/TOB:", (stolenbases+caughtstealing)/(singles+hbp+walks))
print()
sb = round(stolenbases/(stolenbases+caughtstealing), 3)
perseason = 130*((stolenbases+caughtstealing)/(singles+hbp+walks))
print(f"SB per season: {round(perseason*sb)} | CS per season: {round(perseason*(1-sb))}")
print("runs:", runs)
