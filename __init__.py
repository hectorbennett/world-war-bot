"""World War Bot

This program follows a stupid algorithm to determine the ultimate warmonger

it uses country neighbour and population data from https://github.com/lorey/list-of-countries

The procedure works as follows:

    - Pick a random country
    - Pick a random neighbour of that country
    - Choose a probability of victory for the countries based on relative population
    - Choose a winner based on a random number choice and the calculated probability of victory
    - Transfer the loser's population and borders to the winner

Repeat until only one country remains.

Performing this procedure

"""


import os
import sys
import copy
import json
import random

with open(os.path.join(sys.path[0], 'data.json')) as country_data:
    countries = json.loads(country_data.read())

for index, country in enumerate(countries):
    country['neighbours'] = country['neighbours'].split(',')
    country['population'] = int(country['population'])

COUNTRIES = copy.deepcopy(countries)

class World(object):

    def __init__(self):
        self.countries = {}

    def add_country(self, code, name, population):
        self.countries[code] = Country(self, code, name, population)

    def add_border(self, code1, code2):
        self.countries[code1].add_neighbour(self.countries[code2])
        self.countries[code2].add_neighbour(self.countries[code1])


class Country(object):

    def __init__(self, world, code, name, population):
        self.world = world
        self.code = code
        self.name = name
        self.population = population
        self.neighbours = {}

    def add_neighbour(self, other):
        if other.code == self.code:
            return
        self.neighbours[other.code] = other

    def defeat(self, other):
        self.population += other.population
        for neighbour in other.neighbours.values():
            self.add_neighbour(neighbour)
        # self.neighbours.update(other.neighbours)
        for country in self.world.countries.values():
            if other.code in country.neighbours:
                country.add_neighbour(self)
            try:
                del country.neighbours[other.code]
            except KeyError:
                pass
        del self.world.countries[other.code]
        return self

    def challenge_neighbour(self, other):
        if self.name == other.name:
            return

        chance = self.population / float(other.population)

        if self.population >= other.population and random.random() > chance:
            return self.defeat(other)
        return other.defeat(self)

    def __repr__(self):
        return '<{} pop: {}k>'.format(self.name, self.population / 1000)

_earth = World()
for country in COUNTRIES:
    _earth.add_country(country['alpha_2'], country['name'], country['population'])

for country in COUNTRIES:
    for neighbour in country['neighbours']:
        if neighbour == country['alpha_2']:
            continue
        if neighbour:
            _earth.add_border(country['alpha_2'], neighbour)

winners = {}

for _ in range(5000):
    earth = copy.deepcopy(_earth)
    while earth.countries:
        random_choice = random.choice(earth.countries.values())
        if random_choice.neighbours:
            random_neighbour = random.choice(random_choice.neighbours.values())
            winner = random_choice.challenge_neighbour(random_neighbour)
        else:
            del earth.countries[random_choice.code]
    try:
        winners[winner.name] += 1
    except KeyError:
        winners[winner.name] = 1

for country, value in sorted(winners.iteritems()):
    print('{}: {}'.format(country, value))
