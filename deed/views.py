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
		return self.round_number != self.participant.vars['order']

	def vars_for_template(self):
		table_rows = []
		if (self.participant.vars['order'] + 1) != self.round_number:
			if self.participant.vars['order'] != self.round_number & self.round_number != 1:
				prev_player = self.player.in_round(self.round_number - 1)
				row = {
					'round_number': prev_player.round_number,
					'choice': prev_player.choice,
					'outcome': prev_player.outcome,
				}
				table_rows.append(row)

		return {'table_rows': table_rows,
				'order': self.participant.vars['order'],
				'test': (self.participant.vars['order'] + 1) == self.round_number,
		       }

	def before_next_page(self):
		p = random.random()
		if self.player.choice == 'A':
			ch = 1
		else:
			ch = 2
		p_tar = self.participant.vars['stims'][2]['p' + str(ch) + str(1)].iloc[0]
		if p < p_tar:
			payoff = self.participant.vars['stims'][2]['v' + str(ch) + str(1)].iloc[0]
		else:
			payoff = self.participant.vars['stims'][2]['v' + str(ch) + str(2)].iloc[0]
		self.player.outcome = payoff
		if self.round_number == Constants.num_rounds:
				p = self.player.in_round(self.participant.vars['pay_pick']).outcome
				if p > 0:
					self.player.payoff = c(math.log(p) / 10)

class Description(Page):
	form_model = models.Player
	form_fields = ['choice']

	def is_displayed(self):
		return self.round_number == self.participant.vars['order']

	def vars_for_template(self):
		table_rows = []
		row = {
			'choicea': str(int(self.participant.vars['stims'][2]['v11'].iloc[0])) + ' (' + str(int(self.participant.vars['stims'][2]['p11'].iloc[0] * 100)) + '%) or ' +  str(int(self.participant.vars['stims'][2]['v12'].iloc[0])) + ' (' + str(int(self.participant.vars['stims'][2]['p12'].iloc[0] * 100)) + '%)', 
			'choiceb': str(int(self.participant.vars['stims'][2]['v21'].iloc[0])) + ' (' + str(int(self.participant.vars['stims'][2]['p21'].iloc[0] * 100)) + '%) or ' +  str(int(self.participant.vars['stims'][2]['v22'].iloc[0])) + ' (' + str(int(self.participant.vars['stims'][2]['p22'].iloc[0] * 100)) + '%)',
		}
		table_rows.append(row)

		return {'table_rows': table_rows}

	def before_next_page(self):
		p = random.random()
		if self.player.choice == 'A':
			ch = 1
		else: 
			ch = 2
		p_tar = self.participant.vars['stims'][2]['p' + str(ch) + str(1)].iloc[0]
		if p < p_tar:
			payoff = self.participant.vars['stims'][2]['v' + str(ch) + str(1)].iloc[0]
		else:
			payoff = self.participant.vars['stims'][2]['v' + str(ch) + str(2)].iloc[0]
		self.player.outcome = int(payoff)
		if self.round_number == Constants.num_rounds:
			p = self.player.in_round(self.participant.vars['pay_pick']).outcome
			if p > 0:
				self.player.payoff = c(math.log(p) / 10)

class e_intro(Page):
	def is_displayed(self):
		if self.participant.vars['order'] == 1:
			return self.round_number == 2
		else:
			return self.round_number == 1

	def vars_for_template(self):
		if self.round_number == 1:
			return {'inst': 'This is a decision from experience block. For the next 50 rounds, you can choose either A or B, each option is associated with one or more payoff amounts. For fifty choices, you will see the associated payoff but receive no compensation. After that, you will make a final, consequential choice between A and B. The same payoff structure will apply, and this choice will determine your end-of-study payment.'}
		else:
			return{'inst': 'This is a decision from experience block. For the next 50 rounds, you can choose either A or B, each option is associated with one or more payoff amounts. These payoffs will correspond to the explicit description presented in the first round. For fifty choices, you will see the associated payoff but receive no compentation. After that, you will make a final, consequential choice between A and B. The same payoff structure will apply, and this choice will determine your end-of-study payment.'}

class d_intro(Page):
	def is_displayed(self):
		return self.round_number == self.participant.vars['order']

	def vars_for_template(self):
		if self.round_number == 1:
			return {'inst': 'The next page will give you information about a gamble. In this gamble, you can choose either Option A or Option B. Each option will add to or subtract from your points for the study, which will affect your final payoff. You will not receive immediate feedback on the outcome of your choice, but it will be reflected in your final point value.'}
		else:
			return{'inst': 'The next page will give you explicit information about the options from which you have sampled in the previous 50 choices. Please choose either Option A or Option B, which will change your total point value by the amounts and probabilities listed on the next page.'}


class e_consequence(Page):
	def is_displayed(self):
		if self.participant.vars['order'] == 1:
			return self.round_number == Constants.num_rounds
		else:
			return self.round_number == Constants.num_rounds - 1

class Pay(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	def vars_for_template(self):
		return {'current_points': self.player.in_round(self.participant.vars['pay_pick']).outcome,
		        'current_payoff': c(self.participant.payoff),
		       }

page_sequence = [
	e_consequence,
	d_intro,
    Description,
    e_intro,
    Display,
    Pay,
]
