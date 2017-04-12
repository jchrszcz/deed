from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import subprocess
import random
import pandas as pd
import uuid
import os
import math

author = 'J.S. Chrabaszcz'

doc = """
oTree implementation of repeated sampling with final consequential choice, combined experience and description.
"""

def createGamble(certain, reduced):
	p11 = round(random.random() * .9 + .05, 2)
	if certain:
		p21 = 1
	else:
		p21 = round(random.random() * .9 + .05, 2)
	p12 = round(1 - p11, 2)
	p22 = round(1 - p21, 2)
	v11 = round(random.random() * 200 - 100, 1)
	v12 = round(random.random() * 200 - 100, 1)
	ev = p11 * v11 + p12 * v12
	if certain:
		v21 = round(ev, 1)
		v22 = 0
	else:
		if reduced:
			v21 = 0
		else:
			v21 = round(random.random() * 200 - 100, 1)
		v22 = round((ev - p21 * v21) / p22, 1)
	stims = pd.DataFrame({'v11' : v11,
			              'v12' : v12,
			              'v21' : v21,
			              'v22' : v22,
			              'p11' : p11,
			              'p12' : p12,
			              'p21' : p21,
			              'p22' : p22}, index = [0])
	return [certain, reduced, stims]

def stim_setup():
	certain = random.getrandbits(1)
	reduced = random.getrandbits(1)
	if certain == 1 and reduced == 1:
		change = random.getrandbits(1)
		if change == 0:
			certain = 0
		else:
			reduced = 0
	stims = createGamble(certain, reduced)
	return stims

class Constants(BaseConstants):
	name_in_url = 'deed3'
	players_per_group = None
	num_rounds = 52

class Subsession(BaseSubsession):
	def before_session_starts(self):
		if self.round_number == 1:
			for p in self.get_players():
				p.participant.vars['stims'] = stim_setup()
				if random.random() < .5:
					p.participant.vars['order'] = 1
				else:
					p.participant.vars['order'] = Constants.num_rounds
				if random.random() < .5:
					p.participant.vars['pay_pick'] = 1
				else:
					p.participant.vars['pay_pick'] = Constants.num_rounds

class Group(BaseGroup):
    pass

class Player(BasePlayer):
	choice = models.CharField(
		choices=['A', 'B'],
		widget=widgets.RadioSelectHorizontal()
	)

	outcome = models.IntegerField()
