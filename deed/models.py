from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import feather
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

def stim_setup(file_name):
	certain = random.getrandbits(1)
	reduced = random.getrandbits(1)
	if certain == 1 and reduced == 1:
		change = random.getrandbits(1)
		if change == 0:
			certain = 0
		else:
			reduced = 0
	cmd = ['Rscript', '/Users/jchrszcz/Dropbox/ddmlab/deed/oTree/deed/stims.R'] + [file_name, str(certain), str(reduced)]
	x = subprocess.call(cmd)
	stims = feather.read_dataframe(file_name)
	os.remove(file_name)
	return [certain, reduced, stims]

class Constants(BaseConstants):
	name_in_url = 'deed'
	players_per_group = None
	num_rounds = 52

class Subsession(BaseSubsession):
	def before_session_starts(self):
		if self.round_number == 1:
			for p in self.get_players():
				p.participant.vars['stims'] = stim_setup(str(uuid.uuid4()) + '.feather')
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
