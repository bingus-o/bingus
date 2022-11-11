import math
import random
import numpy as np
import names


class Player:
    def __init__(self):
        self.name = names.get_first_name(gender="male")
        self.surname = names.get_last_name()
        self.age = random.randint(20, 35)

        self.max_attr = 99
        if self.age <= 25: self.max_attr = 70+(2*(self.age-20))
        if self.age in [26, 27]: self.max_attr = [85, 90][[26, 27].index(self.age)]

        self.overall = None
        self.position = None
        self.potential = None
        self.salary = None
        self.years_on_contract = None
        self.years_left = None

    def calc_potential(self):
        if 28 < self.age: # peak age or slightly regressing
            self.potential = self.overall + random.randint(0, 5)
        else:
            space = (99-self.overall)
            adder = np.random.normal(loc=space/2, scale=space/4, size=1)[0]
            self.potential = self.overall + adder
            if self.potential > 99: self.potential = 99
            elif self.potential < self.overall: self.potential = self.overall

        self.potential = round(self.potential)

    def calc_salary(self):
        pos, ovr, age = self.position, self.overall, self.age

        avg = {"c": 2500000, "1b": 7000000, "2b": 3800000, "3b": 5400000,
               "ss": 3200000, "rf": 6000000, "cf": 4700000, "lf": 5400000,
               "dh": 6500000, "sp": 5400000, "rp": 2000000, "cp": 4600000}

        max_con = {"c": 16000000, "1b": 24000000, "2b": 19500000, "3b": 30000000,
                   "ss": 28500000, "rf": 22000000, "cf": 25000000, "lf": 18000000,
                   "dh": 23000000, "sp": 37000000, "rp": 19000000, "cp": 13500000}

        min_decrement = (avg[pos] - 700000) / 15
        max_increment = (max_con[pos] - avg[pos]) / 24

        if ovr == 75:
            sal = avg[pos]
        elif ovr < 75:
            sal = avg[pos] - (min_decrement * (75 - ovr))
        else:
            sal = max_con[pos] - (max_increment * (99 - ovr))

        x = np.linspace(sal * 0.8, sal * 1.2)
        mean = np.mean(x)
        sd = np.std(x)
        actual_sal = np.random.normal(loc=mean, scale=sd, size=1)[0]
        actual_sal = round(actual_sal / 100000) * 100000

        years_on_contract = round(((ovr - 60) / 5))
        years_on_contract += random.choice([1, 0, -1])
        if years_on_contract <= 0: years_on_contract = 1

        if age <= 25:
            prob = (-1 / 10) * (age - 20) + 1
            chance = random.choices(population=[True, False], weights=[prob, 1 - prob])[0]
            if chance:  # rookie
                years_on_contract = 1
                actual_sal = 700000
            else:
                if years_on_contract > age - 20: years_on_contract = age - 20

        percent_left = (1 / 15) * (age - 20)
        percent_left += random.choice([0, 0.1, -0.1])
        if percent_left <= 0: percent_left = 0.1
        if percent_left > 1: percent_left = 1

        years_left = math.ceil(percent_left * years_on_contract)

        self.salary = actual_sal
        self.years_on_contract = years_on_contract
        self.years_left = years_left

class Position(Player):
    def __init__(self):
        super().__init__()
        self.position = random.choice(["1b", "2b", "3b", "ss", "lf", "rf","cf", "c", "dh"])

        self.fielding = random.randint(60, self.max_attr)
        self.speed = random.randint(60, self.max_attr)

        self.contact = random.randint(60, self.max_attr)
        self.power = random.randint(60, self.max_attr)
        self.vision = random.randint(60, self.max_attr)

        self.overall = round((self.fielding+self.contact+self.power+self.speed+self.vision)/5)
        self.calc_potential()
        self.calc_salary()

class Pitcher(Player):
    def __init__(self):
        super().__init__()
        self.position = random.choice(["sp", "rp", "cp"])

        self.control = random.randint(60, self.max_attr)
        self.velocity = random.randint(60, self.max_attr)
        self.break_ = random.randint(60, self.max_attr)

        self.overall = round((self.control+self.velocity+self.break_)/3)
        self.calc_potential()
        self.calc_salary()


#gaussian, not random lmf