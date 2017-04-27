from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import subprocess
import random
import pandas as pd
import uuid
import os
import math

class Display(Page):
	form_model = models.Player
	form_fields = ['choice']

	def is_displayed(self):
		return self.round_number != self.participant.vars['order3']

	def vars_for_template(self):
		table_rows = []
		if self.round_number != 1 and self.round_number != Constants.num_rounds:
			if (self.participant.vars['order3'] == 1 and self.round_number != 2) or (self.participant.vars['order3'] == Constants.num_rounds and self.round_number != (Constants.num_rounds - 1)):
				prev_player = self.player.in_round(self.round_number - 1)
				row = {
					'round_number': prev_player.round_number,
					'choice': prev_player.choice,
					'outcome': prev_player.outcome,
				}
				table_rows.append(row)
		if (self.participant.vars['order'] == 1 and self.round_number == Constants.num_rounds) or (self.participant.vars['order'] == Constants.num_rounds and self.round_number == (Constants.num_rounds - 1)):
			title = 'Consequential Choice'
			instruct = 'Based on your experience from the sampling phase, make a choice between A and B. You will NOT receive feedback on this choice bu the outcome will be stored to calculate your bonus payment at the end of the study.'
		else:
			title = 'Experience'
			instruct = 'Before you make a choice between buttons A and B, you will be allowed to explore the points that you gain or lose from each of the buttons by pressing on the buttons and observing the outcomes without any consequences. You will be asked to explore the buttons a total of 20 times during this sampling phase. After the sampling phase, you will then be asked to make one consequential choice. Your bonus payment will depend on the number of points obtained from this consequential choice.'

		return {'table_rows': table_rows,
				'order': self.participant.vars['order3'],
				'title': title,
				'instructions': instruct,
				'test': Constants.num_rounds != self.round_number,
				'test2': not (self.participant.vars['order3'] == 1 and self.round_number != 2),
		       }

	def before_next_page(self):
		p = random.random()
		if self.player.choice == 'A':
			ch = 1
		else:
			ch = 2
		p_tar = self.participant.vars['stims3'][2]['p' + str(ch) + str(1)].iloc[0]
		if p < p_tar:
			payoff = self.participant.vars['stims3'][2]['v' + str(ch) + str(1)].iloc[0]
		else:
			payoff = self.participant.vars['stims3'][2]['v' + str(ch) + str(2)].iloc[0]
		self.player.outcome = payoff
		if self.round_number == Constants.num_rounds:
				p = self.player.in_round(self.participant.vars['pay_pick3']).outcome
				if p > 0:
					self.player.payoff = c(math.log(p) / 10)

class Feedback(Page):
	form_model = models.Player

	def is_displayed(self):
		if self.participant.vars['order3'] == 1:
			return self.round_number == Constants.num_rounds
		else:
			return self.round_number == (Constants.num_rounds - 1)

	def vars_for_template(self):
		table_rows = []
		if (self.participant.vars['order3'] + 1) != self.round_number:
			if self.participant.vars['order3'] != self.round_number & self.round_number != 1:
				prev_player = self.player.in_round(self.round_number - 1)
				row = {
					'round_number': prev_player.round_number,
					'choice': prev_player.choice,
					'outcome': prev_player.outcome,
				}
				table_rows.append(row)

		return {'table_rows': table_rows,
				'order': self.participant.vars['order3'],
				'test': (self.participant.vars['order3'] + 1) == self.round_number,
		       }

class Description(Page):
	form_model = models.Player
	form_fields = ['choice']

	def is_displayed(self):
		return self.round_number == self.participant.vars['order3']

	def vars_for_template(self):
		table_rows = []
		row = {
			'choicea': str(int(self.participant.vars['stims3'][2]['v11'].iloc[0])) + ' (' + str(int(self.participant.vars['stims3'][2]['p11'].iloc[0] * 100)) + '%) or ' +  str(int(self.participant.vars['stims3'][2]['v12'].iloc[0])) + ' (' + str(int(self.participant.vars['stims3'][2]['p12'].iloc[0] * 100)) + '%)', 
			'choiceb': str(int(self.participant.vars['stims3'][2]['v21'].iloc[0])) + ' (' + str(int(self.participant.vars['stims3'][2]['p21'].iloc[0] * 100)) + '%) or ' +  str(int(self.participant.vars['stims3'][2]['v22'].iloc[0])) + ' (' + str(int(self.participant.vars['stims3'][2]['p22'].iloc[0] * 100)) + '%)',
		}
		table_rows.append(row)

		return {'table_rows': table_rows}

	def before_next_page(self):
		p = random.random()
		if self.player.choice == 'A':
			ch = 1
		else: 
			ch = 2
		p_tar = self.participant.vars['stims3'][2]['p' + str(ch) + str(1)].iloc[0]
		if p < p_tar:
			payoff = self.participant.vars['stims3'][2]['v' + str(ch) + str(1)].iloc[0]
		else:
			payoff = self.participant.vars['stims3'][2]['v' + str(ch) + str(2)].iloc[0]
		self.player.outcome = int(payoff)
		if self.round_number == Constants.num_rounds:
			p = self.player.in_round(self.participant.vars['pay_pick3']).outcome
			if p > 0:
				self.player.payoff = c(math.log(p) / 10)

class e_intro(Page):
	def is_displayed(self):
		if self.participant.vars['order3'] == 1:
			return self.round_number == 2
		else:
			return self.round_number == 1

	def vars_for_template(self):
		if self.round_number == 1:
			return {'inst': 'Before you make a choice between buttons A and B, you will be allowed to explore the points that you may gain or lose from each of the buttons by pressing in the buttons and observing the outcomes, without any consequences. You will be asked to explore the buttons a fixed number of times during the sampling phase. After the sampling phase you will then be asked to make one consequential choice. Your bonus payment will depend on the number of points obtained from this consequential choice.'}
		else:
			return{'inst': 'Before you make a choice between buttons A and B, you will be allowed to explore the points that you may gain or lose from each of the buttons by pressing in the buttons and observing the outcomes, without any consequences. You will be asked to explore the buttons a fixed number of times during the sampling phase. After the sampling phase you will then be asked to make one consequential choice. Your bonus payment will depend on the number of points obtained from this consequential choice.'}

class d_intro(Page):
	def is_displayed(self):
		return self.round_number == self.participant.vars['order3']

	def vars_for_template(self):
		if self.round_number == 1:
			return {'inst': 'Please make one choice using the explicit information about two options from which you have already sampled. The description below shows the outcomes (points) and the probability of obtaining that outcome (in parenthesis).'}
		else:
			return{'inst': 'Please make one choice using the explicit information about two options from which you have already sampled. The description below shows the outcomes (points) and the probability of obtaining that outcome (in parenthesis).'}


class e_consequence(Page):
	def is_displayed(self):
		if self.participant.vars['order3'] == 1:
			return self.round_number == Constants.num_rounds
		else:
			return self.round_number == Constants.num_rounds - 1

class Pay(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	def vars_for_template(self):
		return {'current_points': self.player.in_round(self.participant.vars['pay_pick3']).outcome,
		        'current_payoff': c(self.participant.payoff),
		       }

class deed_info(Page):
	def is_displayed(self):
		return self.round_number == 1

page_sequence = [
	Feedback,
    Description,
    Display,
    Pay,
]
